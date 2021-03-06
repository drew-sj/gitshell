#!/usr/bin/python
import re, time
import os, sys
import json
import beanstalkc
from subprocess import Popen
from subprocess import PIPE
from datetime import datetime
from django.core.cache import cache
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from gitshell.gsuser.models import Userprofile, GsuserManager
from gitshell.repo.models import CommitHistory, PushRevRef, Repo, RepoManager, BRANCH_STATUS
from gitshell.feed.models import Feed, NotifMessage, FeedManager
from gitshell.feed.feed import FeedAction
from gitshell.stats.models import StatsManager
from gitshell.daemon.models import EventManager, EVENT_TUBE_NAME, HOOK_TUBE_NAME
from gitshell.settings import REPO_PATH, BEANSTALK_HOST, BEANSTALK_PORT, logger
from gitshell.objectscache.da import da_post_save

MAX_COMMIT_COUNT = 500
def start():
    logger.info('==================== START eventworker ====================')
    beanstalk = beanstalkc.Connection(host=BEANSTALK_HOST, port=BEANSTALK_PORT)
    EventManager.switch(beanstalk, EVENT_TUBE_NAME)
    route_beanstalk_dict = init_route_beanstalk_dict()
    while True:
        event_job = beanstalk.reserve()
        try:
            event = json.loads(event_job.body)
            # exit signal
            if event['type'] == -1:
                event_job.delete()
                sys.exit(0)
            do_event(event)
            do_route_event(route_beanstalk_dict, event_job)
        except Exception, e:
            logger.error('do_event catch except, event: %s' % event_job.body)
            logger.exception(e)
        event_job.delete()
    logger.info('==================== STOP eventworker ====================')

def init_route_beanstalk_dict():
    route_beanstalk_dict = {}
    for tube_name in [HOOK_TUBE_NAME]:
        beanstalk = beanstalkc.Connection(host=BEANSTALK_HOST, port=BEANSTALK_PORT)
        EventManager.switch(beanstalk, tube_name)
        route_beanstalk_dict[tube_name] = beanstalk
    return route_beanstalk_dict

def do_route_event(route_beanstalk_dict, event_job):
    for tube_name, beanstalk in route_beanstalk_dict.iteritems():
        beanstalk.put(event_job.body)

# abspath is the repo hooks directory
def do_event(event):
    etype = event['type']
    diff_tree_blob_size_params = []
    if etype == 0:
        abspath = event['abspath'].strip()
        if abspath.endswith('/'):
            abspath = abspath[0 : len(abspath)-1]
        (username, reponame) = get_username_reponame(abspath)
        if username == '' or reponame == '':
            return
        (user, userprofile, repo, repopath) = get_user_repo_attr(username, reponame)
        if user is None or userprofile is None or repo is None or repopath is None or not os.path.exists(repopath):
            return
        __clear_relative_cache(user, userprofile, repo)
        remote_username = event['remote_user']; push_timestamp = event['push_timestamp']; rev_ref_arr = event['revrefarr']
        pushUser = get_push_user(remote_username, user); push_id = long(push_timestamp)
        commit_count = 0
        for rev_ref in rev_ref_arr:
            if len(rev_ref) < 3:
                continue
            oldrev = rev_ref[0]; newrev = rev_ref[1]; refname = rev_ref[2]
            diff_tree_blob_size_params.extend(rev_ref)
            commit_count = bulk_create_commits(user, userprofile, repo, repopath, push_id, pushUser, oldrev, newrev, refname) + commit_count
            if commit_count > MAX_COMMIT_COUNT:
                break
        repo.commit = repo.commit + commit_count
        repo.last_push_time = datetime.now()
        update_quote(user, userprofile, repo, repopath, diff_tree_blob_size_params)
        return

def update_quote(user, userprofile, repo, repopath, parameters):
    args = ['/opt/bin/diff-tree-blob-size.sh', repopath]
    args.extend(parameters)
    popen = Popen(args, stdout=PIPE, shell=False, close_fds=True)
    result = popen.communicate()[0].strip()
    diff_size = 0
    if popen.returncode == 0:
        if result.startswith('+') or result.startswith('-'):
            diff_size = int(result)
        else:
            diff_size = int(result) - repo.used_quote
    RepoManager.update_user_repo_quote(userprofile, repo, diff_size)

# git log -100 --pretty='%h  %p  %t  %an  %cn  %ct  %ce  %ae  %s'
def bulk_create_commits(user, userprofile, repo, repopath, push_id, pushUser, oldrev, newrev, refname):

    # list raw commitHistorys
    raw_commitHistorys = __list_raw_commitHistorys(repo, repopath, oldrev, newrev, refname)

    # list uniq commitHistorys and convert to pushRevRef
    commitHistorys = __list_not_exists_commitHistorys(repo, raw_commitHistorys)
    if len(commitHistorys) == 0:
        return 0
    (pushRevRef, commitHistorys) = __create_pushRevRef_and_save(repo, commitHistorys, push_id, pushUser, oldrev, newrev, refname)

    feedAction = FeedAction()
    # generate feed data
    push_revref_feed = __get_push_revref_feed(repo, pushRevRef)
    __add_user_and_repo_feed(feedAction, userprofile, repo, pushRevRef, push_revref_feed)

    # user username, email dict
    (member_username_dict, member_email_dict) = __get_member_username_email_dict(repo)

    # at somebody action
    __notif(commitHistorys, repo, member_username_dict, member_email_dict)

    # stats action
    __stats(feedAction, commitHistorys, repo, member_username_dict, member_email_dict)
    
    return len(commitHistorys)

def get_committer_id(repo, commitHistory, member_username_dict, member_email_dict):
    if len(member_username_dict) == 1:
        return repo.user_id
    elif commitHistory.committer in member_username_dict:
        return member_username_dict[commitHistory.committer]
    elif commitHistory.committer_email in member_email_dict:
        return member_email_dict[commitHistory.committer_email]
    return None

def get_author_id(repo, commitHistory, member_username_dict, member_email_dict):
    if len(member_username_dict) == 1:
        return repo.user_id
    elif commitHistory.author in member_username_dict:
        return member_username_dict[commitHistory.author]
    elif commitHistory.author_email in member_email_dict:
        return member_email_dict[commitHistory.author_email]
    return None

def __get_push_revref_feed(repo, pushRevRef):
    feed = Feed.create_push_revref(pushRevRef.push_user_id, repo.id, pushRevRef.id)
    feed.save()
    return feed

def __create_pushRevRef_and_save(repo, commitHistorys, push_id, pushUser, oldrev, newrev, refname):
    old_commit_hash=oldrev[0:7]; new_commit_hash=newrev[0:7]
    pushRevRef = PushRevRef(push_id=push_id, push_user_id=pushUser.id, repo_id=repo.id, old_commit_hash=old_commit_hash, new_commit_hash=new_commit_hash, refname=refname)
    status = BRANCH_STATUS.UPDATE
    if oldrev.startswith('000000') and not newrev.startswith('000000'):
        status = BRANCH_STATUS.CREATE
    if not oldrev.startswith('000000') and newrev.startswith('000000'):
        status = BRANCH_STATUS.DELETE
    pushRevRef.status = status
    pushRevRef.save()
    for commitHistory in commitHistorys:
        commitHistory.pushrevref_id = pushRevRef.id
        commitHistory.save()
    return (pushRevRef, commitHistorys)

def __get_member_username_email_dict(repo):
    member_userprofiles = RepoManager.list_repo_team_memberUser(repo.id)
    member_username_dict = dict([(x.username, x.id) for x in member_userprofiles])
    member_email_dict = dict([(x.email, x.id) for x in member_userprofiles])
    return (member_username_dict, member_email_dict)

def __add_user_and_repo_feed(feedAction, userprofile, repo, pushRevRef, push_revref_feed):
    feed_key_value = [-float(pushRevRef.push_id), push_revref_feed.id]
    if userprofile.is_team_account == 1:
        feedAction.madd_pri_user_feed(userprofile.id, feed_key_value)
    if repo.auth_type == 2:
        feedAction.madd_pri_user_feed(pushRevRef.push_user_id, feed_key_value)
    else:
        feedAction.madd_pub_user_feed(pushRevRef.push_user_id, feed_key_value)
    feedAction.madd_repo_feed(repo.id, feed_key_value)
    feedAction.madd_latest_feed(feed_key_value)

def __list_raw_commitHistorys(repo, repopath, oldrev, newrev, refname):
    args = ['/opt/bin/git-pretty-log.sh', repopath, oldrev, newrev]
    popen = Popen(args, stdout=PIPE, shell=False, close_fds=True)
    result = popen.communicate()[0].strip()
    raw_commitHistorys = []
    if popen.returncode == 0:
        for line in result.split('\n'):
            items = line.split('______', 8)
            if len(items) >= 9 and re.match('^\d+$', items[5]):
                committer_date = datetime.fromtimestamp(int(items[5])) 
                author_name = items[3][0:30]
                committer_name = items[4][0:30]
                commitHistory = CommitHistory.create(repo.id, repo.name, items[0], items[1][0:24], items[2], author_name, committer_name, committer_date, items[8][0:512], refname[0:32], items[6], items[7])
                raw_commitHistorys.append(commitHistory)
    return raw_commitHistorys

def __list_not_exists_commitHistorys(repo, raw_commitHistorys):
    commitHistorys = []
    commit_ids = [x.commit_id for x in raw_commitHistorys]
    exists_commitHistorys = RepoManager.list_commits_by_commit_ids(repo.id, commit_ids)
    exists_commit_ids_set = set([x.commit_id for x in exists_commitHistorys])
    commitHistorys = []
    for commitHistory in raw_commitHistorys:
        if commitHistory.commit_id not in exists_commit_ids_set:
            commitHistorys.append(commitHistory)
    return commitHistorys

def __notif(commitHistorys, repo, member_username_dict, member_email_dict):
    for commitHistory in commitHistorys:
        from_user_id = get_author_id(repo, commitHistory, member_username_dict, member_email_dict)
        if from_user_id is not None:
            FeedManager.notif_commit_at(from_user_id, commitHistory.id, commitHistory.subject)
    
def __stats(feedAction, commitHistorys, repo, member_username_dict, member_email_dict):
    unique_author_ids = {}
    stats_commits = []
    for commitHistory in commitHistorys:
        committer_id = get_committer_id(repo, commitHistory, member_username_dict, member_email_dict)
        author_id = get_author_id(repo, commitHistory, member_username_dict, member_email_dict)
        if committer_id is not None and author_id is not None:
            timestamp = time.mktime(commitHistory.committer_date.timetuple())
            stats_commits.append([repo.id, committer_id, author_id, timestamp])
            if author_id not in unique_author_ids:
                unique_author_ids[author_id] = 1
    for unique_author_id in unique_author_ids.keys():
        feedAction.add_recently_active_repo_now(unique_author_id, repo.id)
    StatsManager.stats(stats_commits)

def __clear_relative_cache(user, userprofile, repo):
    RepoManager.delete_repo_commit_version(repo)
    
def get_username_reponame(abspath):
    rfirst_slash_idx = abspath.rfind('/')
    rsecond_slash_idx = abspath.rfind('/', 0, rfirst_slash_idx)
    rthird_slash_idx = abspath.rfind('/', 0, rsecond_slash_idx)
    if rthird_slash_idx > 0 and rthird_slash_idx < rsecond_slash_idx and rsecond_slash_idx < rfirst_slash_idx:
        (username, reponame) = (abspath[rthird_slash_idx+1 : rsecond_slash_idx], abspath[rsecond_slash_idx+1 : rfirst_slash_idx])
        if reponame.endswith('.git'):
            reponame = reponame[0 : len(reponame)-4]
        return (username, reponame)
    return ('', '')

def get_push_user(remote_username, user):
    remote_user = GsuserManager.get_user_by_name(remote_username)
    if remote_user:
        return remote_user
    return user

def get_user_repo_attr(username, reponame):
    nones = (None, None, None, None)
    user = GsuserManager.get_user_by_name(username) 
    if not user:
        return nones
    userprofile = GsuserManager.get_userprofile_by_id(user.id)
    if not userprofile:
        return nones
    repo = RepoManager.get_repo_by_userId_name(user.id, reponame)
    if not repo:
        return nones
    abs_repopath = repo.get_abs_repopath()
    return (user, userprofile, repo, abs_repopath)

def stop():
    EventManager.send_stop_event(EVENT_TUBE_NAME)
    print 'send stop event message...'

def __cache_version_update(sender, **kwargs):
    da_post_save(kwargs['instance'])

if __name__ == '__main__':
    post_save.connect(__cache_version_update)
    post_delete.connect(__cache_version_update)
    if len(sys.argv) < 2:
        sys.exit(1)
    action = sys.argv[1]
    if action == 'start':
        start()
    elif action == 'stop':
        stop()

