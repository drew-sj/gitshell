import re
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from gitshell.repos.models import ReposManager
from gitshell.gsuser.models import UserprofileManager
from gitshell.keyauth.models import UserPubkey, KeyauthManager
from gitshell.dist.views import repos as dist_repos

def pubkey(request, fingerprint):
    userPubkey = KeyauthManager.get_userpubkey_by_fingerprint(fingerprint)
    if userPubkey is not None:
        return HttpResponse(userPubkey.key, content_type="text/plain")
    return HttpResponse("", content_type="text/plain")

def keyauth(request, fingerprint, command):
    command = command.strip()
    last_blank_idx = command.rfind(' ')
    if last_blank_idx == -1:
        return not_git_command()
    pre_command = command[0 : last_blank_idx]
    short_repos_path = command[last_blank_idx+1 :]
    if pre_command == '' or '"' in pre_command or '\'' in pre_command or short_repos_path == '':
        return not_git_command()

    first_repos_char_idx = -1
    slash_idx = -1
    last_repos_char_idx = -1
    for i in range(0, len(short_repos_path)):
        schar = short_repos_path[i]
        if first_repos_char_idx == -1 and re.match('\w', schar):
            first_repos_char_idx = i
        if schar == '/':
            slash_idx = i
        if re.match('\w', schar):
            last_repos_char_idx = i
    if not (first_repos_char_idx > -1 and first_repos_char_idx < slash_idx and slash_idx < last_repos_char_idx):
        return not_git_command()

    username = short_repos_path[first_repos_char_idx : slash_idx] 
    reposname = short_repos_path[slash_idx+1 : last_repos_char_idx+1]
    if not (re.match('^\w+$', username) and re.match('^\w+$', reposname)):
        return not_git_command()
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return not_git_command()

    repos = ReposManager.get_repos_by_userId_name(user.id, reposname)
    if repos is not None:
        pre_repos_path = '/opt/repos/private'
        if repos.auth_type == 0:
            pre_repos_path = '/opt/repos/public' 
        userprofile = UserprofileManager.get_userprofile_by_id(user.id)
        if userprofile.used_quote > userprofile.quote:
            return not_git_command()

        quote = userprofile.quote
        userPubkey = KeyauthManager.get_userpubkey_by_userId_fingerprint(user.id, fingerprint)
        if userPubkey is not None:
            return response_full_git_command(quote, pre_command, pre_repos_path, username, reposname)
        # member of repos TODO
    return not_git_command()

blocks_quote = {67108864 : 32768}
kbytes_quote = {67108864 : 16384}
def response_full_git_command(quote, pre_command, pre_repos_path, username, reposname):
    blocks = 32768
    kbytes = 16384
    if quote in blocks_quote:
        blocks = blocks_quote[quote]
        kbytes = kbytes_quote[quote]
    return HttpResponse("ulimit -f %s && ulimit -m %s && ulimit -v %s && /usr/bin/git-shell -c \"%s '%s/%s/%s'\"" % (blocks, kbytes, kbytes, pre_command, pre_repos_path, username, reposname), content_type="text/plain")

def not_git_command():
    return HttpResponse("echo 'fatal: git repository size limit exceeded or you have not rights or does not appear to be a git command'", content_type="text/plain")

# echo -e "       _ _       _          _ _ \n      (_) |     | |        | | |\n  __ _ _| |_ ___| |__   ___| | |\n / _\` | | __/ __| '_ \ / _ \ | |\n| (_| | | |_\__ \ | | |  __/ | |\n \__, |_|\__|___/_| |_|\___|_|_|\n  __/ |                         \n |___/                          \nusage\n    help: get the help message\n    ls yourname: ls yournam's repos\n    mkdir yourname/reposname: create private repos for user yourname\n"

