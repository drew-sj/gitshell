# -*- coding: utf-8 -*-  
import os, re
import shutil
import json
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from gitshell.feed.feed import FeedAction
from gitshell.repos.Forms import ReposForm
from gitshell.repos.githandler import GitHandler
from gitshell.repos.models import Repos, ReposManager
from gitshell.settings import PRIVATE_REPOS_PATH, PUBLIC_REPOS_PATH, GIT_BARE_REPOS_PATH

@login_required
def user_repos(request, user_name):
    return user_repos_paging(request, user_name, 0)

@login_required
def user_repos_paging(request, user_name, pagenum):
    repos_list = ReposManager.list_repos_by_userId(request.user.id, 0, 25)
    repos_commit_map = {}
    feedAction = FeedAction()
    for repos in repos_list:
        repos_commit_map[str(repos.name)] = []
        feeds = feedAction.get_repos_feeds(repos.id, 0, 4)
        for feed in feeds:
            repos_commit_map[str(repos.name)].append(feed[0])
    response_dictionary = {'user_name': user_name, 'repos_list': repos_list, 'repos_commit_map': repos_commit_map}
    return render_to_response('repos/user_repos.html',
                          response_dictionary,
                          context_instance=RequestContext(request))

def repos(request, user_name, repo_name):
    refs = 'master'
    path = '.'
    current = 'index'
    return repos_ls_tree(request, user_name, repo_name, refs, path, current)

def repos_tree(request, user_name, repo_name, refs, path):
    current = 'tree'
    return repos_ls_tree(request, user_name, repo_name, refs, path, current)

lang_suffix = {'applescript': 'AppleScript', 'as3': 'AS3', 'bash': 'Bash', 'sh': 'Bash', 'cfm': 'ColdFusion', 'cfc': 'ColdFusion', 'cpp': 'Cpp', 'cxx': 'Cpp', 'c': 'Cpp', 'h': 'Cpp', 'cs': 'CSharp', 'css': 'Css', 'dpr': 'Delphi', 'dfm': 'Delphi', 'pas': 'Delphi', 'diff': 'Diff', 'patch': 'Diff', 'erl': 'Erlang', 'groovy': 'Groovy', 'fx': 'JavaFX', 'jfx': 'JavaFX', 'java': 'Java', 'js': 'JScript', 'pl': 'Perl', 'py': 'Python', 'php': 'Php', 'psl': 'PowerShell', 'rb': 'Ruby', 'sass': 'Sass', 'scala': 'Scala', 'sql': 'Sql', 'vb': 'Vb', 'xml': 'Xml', 'xhtml': 'Xml', 'html': 'Xml', 'htm': 'Xml'}
brush_aliases = {'AppleScript': 'applescript', 'AS3': 'actionscript3', 'Bash': 'shell', 'ColdFusion': 'coldfusion', 'Cpp': 'cpp', 'CSharp': 'csharp', 'Css': 'css', 'Delphi': 'delphi', 'Diff': 'diff', 'Erlang': 'erlang', 'Groovy': 'groovy', 'JavaFX': 'javafx', 'Java': 'java', 'JScript': 'javascript', 'Perl': 'perl', 'Php': 'php', 'Plain': 'plain', 'PowerShell': 'powershell', 'Python': 'python', 'Ruby': 'ruby', 'Sass': 'sass', 'Scala': 'scala', 'Sql': 'sql', 'Vb': 'vb', 'Xml': 'xml'}
def repos_ls_tree(request, user_name, repo_name, refs, path, current):
    repo = get_repo_by_name(user_name, repo_name)
    if repo is None:
        raise Http404
    if path is None or path == '':
        path = '.'
    gitHandler = GitHandler()
    abs_repopath = repo.get_abs_repopath(user_name)
    commit_hash = gitHandler.get_commit_hash(abs_repopath, refs)
    is_tree = True ; tree = {} ; blob = ''; lang = 'Plain'; brush = 'plain'
    if path == '.' or path.endswith('/'):
        tree = gitHandler.repo_ls_tree(abs_repopath, commit_hash, path)
    else:
        is_tree = False
        paths = path.split('.')
        if len(paths) > 0:
            suffix = paths[-1]
            if suffix in lang_suffix and lang_suffix[suffix] in brush_aliases:
                lang = lang_suffix[suffix]
                brush = brush_aliases[lang]
        blob = gitHandler.repo_cat_file(abs_repopath, commit_hash, path)
    response_dictionary = {'current': current, 'repo': repo, 'user_name': user_name, 'repos_name': repo_name, 'refs': refs, 'path': path, 'tree': tree, 'blob': blob, 'is_tree': is_tree, 'lang': lang, 'brush': brush}
    return render_to_response('repos/tree.html',
                          response_dictionary,
                          context_instance=RequestContext(request))

def repos_commits(request, user_name, repos_name):
    response_dictionary = {'current': 'commits', 'user_name': user_name, 'repos_name': repos_name}
    return render_to_response('repos/repos.html',
                          response_dictionary,
                          context_instance=RequestContext(request))

def repos_issues(request, user_name, repos_name):
    response_dictionary = {'current': 'issues', 'user_name': user_name, 'repos_name': repos_name}
    return render_to_response('repos/repos.html',
                          response_dictionary,
                          context_instance=RequestContext(request))

def repos_network(request, user_name, repos_name):
    response_dictionary = {'current': 'network', 'user_name': user_name, 'repos_name': repos_name}
    return render_to_response('repos/repos.html',
                          response_dictionary,
                          context_instance=RequestContext(request))

def repos_branches(request, user_name, repos_name):
    response_dictionary = {'current': 'branches', 'user_name': user_name, 'repos_name': repos_name}
    return render_to_response('repos/repos.html',
                          response_dictionary,
                          context_instance=RequestContext(request))

def repos_stats(request, user_name, repos_name):
    response_dictionary = {'current': 'stats', 'user_name': user_name, 'repos_name': repos_name}
    return render_to_response('repos/repos.html',
                          response_dictionary,
                          context_instance=RequestContext(request))

def repo_refs(request, user_name, repo_name):
    repo = get_repo_by_name(user_name, repo_name)
    if repo is None:
        return HttpResponse(json.dumps({'user_name': user_name, 'repo_name': repo_name, 'branches': [], 'tags': []}), mimetype="application/json")
    repopath = repo.get_abs_repopath(user_name)

    gitHandler = GitHandler()
    branches_refs = gitHandler.repo_ls_branches(repopath)
    tags_refs = gitHandler.repo_ls_tags(repopath)
    response_dictionary = {'user_name': user_name, 'repo_name': repo_name, 'branches': branches_refs, 'tags': tags_refs}
    return HttpResponse(json.dumps(response_dictionary), mimetype="application/json")

def get_repo_by_name(user_name, repo_name):
    try:
        user = User.objects.get(username=user_name)     
        return ReposManager.get_repos_by_userId_name(user.id, repo_name)
    except User.DoesNotExist:
        return None

def folder(request):
    response_dictionary = {'hello_world': 'hello world'}
    return render_to_response('repos/folder.html',
                          response_dictionary,
                          context_instance=RequestContext(request))

def file(request):
    response_dictionary = {'hello_world': 'hello world'}
    return render_to_response('repos/file.html',
                          response_dictionary,
                          context_instance=RequestContext(request))						  
# TODO
@login_required
def edit(request, rid):
    error = u''
    repos = Repos()
    if rid != '0':
        try:
            repos = Repos.objects.get(id = rid, user_id = request.user.id)
        except Repos.DoesNotExist:
            pass
    reposForm = ReposForm(instance = repos)
    repos.user_id = request.user.id
    if request.method == 'POST':
        reposForm = ReposForm(request.POST, instance = repos)
        if reposForm.is_valid() and re.match("^\w+$", reposForm.cleaned_data['name']):
            fulfill_gitrepos(request.user.username, reposForm.cleaned_data['name'], reposForm.cleaned_data['auth_type'])
            reposForm.save()
            return HttpResponseRedirect('/' + request.user.username + '/repos/')
        else:
            error = u'输入正确的仓库名称[A-Za-z0-9_]，选择好语言和可见度'
    response_dictionary = {'reposForm': reposForm, 'rid': rid, 'error': error}
    return render_to_response('repos/edit.html',
                          response_dictionary,
                          context_instance=RequestContext(request))

def get_commits_by_ids(ids):
    return ReposManager.get_commits_by_ids(ids)

def fulfill_gitrepos(username, reposname, auth_type):
    for base_repos_path in [PUBLIC_REPOS_PATH, PRIVATE_REPOS_PATH]:
        user_repos_path = '%s/%s' % (base_repos_path, username)
        if not os.path.exists(user_repos_path):
            os.makedirs(user_repos_path)
    pub_repos_path = ('%s/%s/%s.git' % (PUBLIC_REPOS_PATH, username, reposname))
    pri_repos_path = ('%s/%s/%s.git' % (PRIVATE_REPOS_PATH, username, reposname))
    if auth_type == '0': 
        if not os.path.exists(pub_repos_path):
            if os.path.exists(pri_repos_path):
                shutil.move(pri_repos_path, pub_repos_path)
            else:
                shutil.copytree(GIT_BARE_REPOS_PATH, pub_repos_path)             
    else:
        if not os.path.exists(pri_repos_path):
            if os.path.exists(pub_repos_path):
                shutil.move(pub_repos_path, pri_repos_path)
            else:
                shutil.copytree(GIT_BARE_REPOS_PATH, pri_repos_path)             


