from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('gitshell',
    # gitshell web app, nginx port 8000, proxy by haproxy, public
    url(r'^/?$', 'feed.views.index'),

    # explore
    url(r'^explore/?$', 'explore.views.explore'),

    # ajax
    url(r'^ajax/user/find/?$', 'gsuser.views.find'),
    url(r'^ajax/user/change/?$', 'gsuser.views.change'),
    url(r'^ajax/user/watch/(\w+)/', 'gsuser.views.watch'),
    url(r'^ajax/user/unwatch/(\w+)/', 'gsuser.views.unwatch'),
    url(r'^ajax/feed/ids/?$', 'feed.views.feed_by_ids'),
    url(r'^ajax/repo/find/?$', 'repo.views.find'),
    url(r'^ajax/repo/list/github/?$', 'repo.views.list_github_repos'),
    url(r'^ajax/home/do_issue/?$', 'issue.views.do_issue'),

    # dashboard
    url(r'^dashboard/?$', 'feed.views.dashboard'),
    url(r'^dashboard/feed/?$', 'feed.views.feed'),
    url(r'^dashboard/timeline/?$', 'feed.views.timeline'),
    url(r'^dashboard/todo/?$', 'todolist.views.todo'),
    url(r'^dashboard/todo/(\d+)/?$', 'todolist.views.todo_scene'),
    url(r'^dashboard/todo/(\d+)/add/?$', 'todolist.views.add_scene'),
    url(r'^dashboard/todo/(\d+)/remove/?$', 'todolist.views.remove_scene'),
    url(r'^dashboard/todo/(\d+)/add_todo/?$', 'todolist.views.add_todo'),
    url(r'^dashboard/todo/(\d+)/remove_todo/?$', 'todolist.views.remove_todo'),
    url(r'^dashboard/todo/(\d+)/doing_todo/?$', 'todolist.views.doing_todo'),
    url(r'^dashboard/todo/(\d+)/done_todo/?$', 'todolist.views.done_todo'),
    url(r'^dashboard/todo/(\d+)/update_scene_meta/?$', 'todolist.views.update_scene_meta'),
    url(r'^dashboard/issues/?$', 'feed.views.issues_default'),
    url(r'^dashboard/issues/(\d+)/?$', 'feed.views.issues'),
    url(r'^dashboard/pull/?$', 'feed.views.pull_merge'),
    url(r'^dashboard/pull/merge/?$', 'feed.views.pull_merge'),
    url(r'^dashboard/pull/request/?$', 'feed.views.pull_request'),
    url(r'^dashboard/notif/?$', 'feed.views.notif'),
    url(r'^dashboard/explore/?$', 'feed.views.explore'),

    url(r'^([a-zA-Z0-9_-]+)/-/dashboard/?$', 'team.views.dashboard'),
    url(r'^([a-zA-Z0-9_-]+)/-/dashboard/timeline/?$', 'team.views.timeline'),
    url(r'^([a-zA-Z0-9_-]+)/-/dashboard/issues/?$', 'team.views.issues_default'),
    url(r'^([a-zA-Z0-9_-]+)/-/dashboard/issues/(\d+)/?$', 'team.views.issues'),
    url(r'^([a-zA-Z0-9_-]+)/-/dashboard/pull/?$', 'team.views.pull_merge'),
    url(r'^([a-zA-Z0-9_-]+)/-/dashboard/pull/merge/?$', 'team.views.pull_merge'),
    url(r'^([a-zA-Z0-9_-]+)/-/dashboard/pull/request/?$', 'team.views.pull_request'),
    url(r'^([a-zA-Z0-9_-]+)/-/dashboard/notif/?$', 'team.views.notif'),
    url(r'^([a-zA-Z0-9_-]+)/-/dashboard/repo/?$', 'team.views.repo'),

    # settings
    url(r'^settings/?$', 'gssettings.views.profile'),
    url(r'^settings/profile/?$', 'gssettings.views.profile'),
    url(r'^settings/sshpubkey/?$', 'gssettings.views.sshpubkey'),
    url(r'^settings/sshpubkey/remove/?$', 'gssettings.views.sshpubkey_remove'),
    url(r'^settings/emails/?$', 'gssettings.views.emails'),
    url(r'^settings/email/add/?$', 'gssettings.views.email_add'),
    url(r'^settings/email/primary/(\d+)/?$', 'gssettings.views.email_primary'),
    url(r'^settings/email/verify/(\d+)/?$', 'gssettings.views.email_verify'),
    url(r'^settings/email/verified/(\w+)/?$', 'gssettings.views.email_verified'),
    url(r'^settings/email/remove/(\d+)/?$', 'gssettings.views.email_remove'),
    url(r'^settings/notif/?$', 'gssettings.views.notif'),
    url(r'^settings/notif/types/?$', 'gssettings.views.notif_types'),
    url(r'^settings/notif/fqcy/?$', 'gssettings.views.notif_fqcy'),
    url(r'^settings/notif/email/?$', 'gssettings.views.notif_email'),
    url(r'^settings/changepassword/?$', 'gssettings.views.changepassword'),
    url(r'^settings/thirdparty/?$', 'gssettings.views.thirdparty'),
    url(r'^settings/change_username_email/?$', 'gssettings.views.change_username_email'),
    url(r'^settings/validate_email/(\w+)/?$', 'gssettings.views.validate_email'),
    url(r'^settings/team/?$', 'gssettings.views.team'),
    url(r'^settings/team/create/?$', 'gssettings.views.team_create'),
    url(r'^settings/team/leave/?$', 'gssettings.views.team_leave'),
    url(r'^settings/destroy/?$', 'gssettings.views.destroy'),

    url(r'^([a-zA-Z0-9_-]+)/-/settings/?$', 'team.views.settings'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/profile/?$', 'team.views.profile'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/members/?$', 'team.views.members'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/team/member/leave/?$', 'team.views.member_leave'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/team/member/add/?$', 'team.views.add_member'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/team/member/remove/?$', 'team.views.remove_member'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/team/member/grant/admin/?$', 'team.views.grant_admin'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/team/member/cancal/admin/?$', 'team.views.cancal_admin'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/groups/?$', 'team.views.groups'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/group/(\d+)/?$', 'team.views.group'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/group/add/?$', 'team.views.group_add'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/group/remove/?$', 'team.views.group_remove'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/group/add_member/?$', 'team.views.group_add_member'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/group/remove_member/?$', 'team.views.group_remove_member'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/destroy/?$', 'team.views.destroy'),
    url(r'^([a-zA-Z0-9_-]+)/-/settings/destroy_confirm/?$', 'team.views.destroy_confirm'),

    # user login logout join
    url(r'^login/?$', 'gsuser.views.login'),
    url(r'^login/oauth/github/?$', 'gsuser.views.login_github'),
    url(r'^login/oauth/github/apply/?$', 'gsuser.views.login_github_apply'),
    url(r'^login/oauth/github/relieve/?$', 'gsuser.views.login_github_relieve'),
    url(r'^logout/?$', 'gsuser.views.logout'),
    url(r'^join/ref/(\w+)/?$', 'gsuser.views.join_via_ref'),
    url(r'^join/?(\w+)?/?$', 'gsuser.views.join'),
    url(r'^bind/(\w+)/?$', 'gsuser.views.bind'),
    url(r'^resetpassword/?(\w+)?/?$', 'gsuser.views.resetpassword'),

    # help
    url(r'^help/?$', 'help.views.default'),
    url(r'^help/quickstart/?$', 'help.views.quickstart'),
    url(r'^help/error/?$', 'help.views.error'),
    url(r'^help/error/(\w+)/?$', 'help.views.error_with_reason'),
    url(r'^help/reset_access_limit/?$', 'help.views.reset_access_limit'),

    # gitshell openssh keyauth and dist, private for subnetwork access by iptables, nginx port 9000
    url(r'^private/http_auth/?$', 'keyauth.views.http_auth'),
    url(r'^private/keyauth/([a-zA-Z0-9:]+)/?$', 'keyauth.views.pubkey'),
    url(r'^private/keyauth/([a-zA-Z0-9:]+)/([a-zA-Z0-9_ "\-\'\/\.]+)$', 'keyauth.views.keyauth'),
    url(r'^private/dist/repo/(\w+)/([a-zA-Z0-9_\-]+)/?$', 'dist.views.repo'),
    url(r'^private/dist/refresh/?$', 'dist.views.refresh'),
    url(r'^private/dist/echo/?$', 'dist.views.echo'),

    # gitshell keep namespace
    url(r'^gitshell/list_latest_push_repo/(\w+)/?$', 'repo.views.list_latest_push_repo'),

    # third part
    url(r'^captcha/', include('captcha.urls')),

    # gsuser
    url(r'^([a-zA-Z0-9_-]+)/?$', 'gsuser.views.user'),
    url(r'^([a-zA-Z0-9_-]+)/-/user/switch/(\d+)/?$', 'gsuser.views.switch'),
    url(r'^([a-zA-Z0-9_-]+)/-/stats/?$', 'gsuser.views.stats'),
    url(r'^([a-zA-Z0-9_-]+)/-/active/?$', 'gsuser.views.active'),
    url(r'^([a-zA-Z0-9_-]+)/-/star/repo/?$', 'gsuser.views.star_repo'),
    url(r'^([a-zA-Z0-9_-]+)/-/watch/repo/?$', 'gsuser.views.watch_repo'),
    url(r'^([a-zA-Z0-9_-]+)/-/watch/user/?$', 'gsuser.views.watch_user'),
    url(r'^([a-zA-Z0-9_-]+)/-/repo/?$', 'repo.views.user_repo'),
    url(r'^([a-zA-Z0-9_-]+)/-/repo/(\d+)/?$', 'repo.views.user_repo_paging'),
    url(r'^([a-zA-Z0-9_-]+)/-/repo/recently/?$', 'repo.views.recently'),
    url(r'^([a-zA-Z0-9_-]+)/-/repo/create/?$', 'repo.views.create'),

    # repo
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/?$', 'repo.views.repo'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/tree/?$', 'repo.views.tree_default'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/tree/([a-zA-Z0-9_\.\-]+)/([^\@\#\$\&\\\*\"\'\<\>\|\;]*)$', 'repo.views.tree'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/tree_ajax/([a-zA-Z0-9_\.\-]+)/([^\@\#\$\&\\\*\"\'\<\>\|\;]*)$', 'repo.views.tree_ajax'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/blob/([a-zA-Z0-9_\.\-]+)/([^\@\#\$\&\\\*\"\'\<\>\|\;]*)$', 'repo.views.blob'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/blob_ajax/([a-zA-Z0-9_\.\-]+)/([^\@\#\$\&\\\*\"\'\<\>\|\;]*)$', 'repo.views.blob_ajax'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/raw/blob/([a-zA-Z0-9_\.\-]+)/([^\@\#\$\&\\\*\"\'\<\>\|\;]*)$', 'repo.views.raw_blob'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/commit/([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.commit'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/commits/?$', 'repo.views.commits_default'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/commits/([a-zA-Z0-9_\.\-]+)\.\.\.([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.commits_log'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/commits/([a-zA-Z0-9_\.\-]+)/([^\@\#\$\&\\\*\"\'\<\>\|\;]*)$', 'repo.views.commits'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/branches/?$', 'repo.views.branches_default'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/branches/([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.branches'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/tags/?$', 'repo.views.tags_default'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/tags/([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.tags'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/compare/?$', 'repo.views.compare_default'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/compare/([a-zA-Z0-9_\.\-]+)\.\.\.([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.compare_commit'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/compare/([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.compare_master'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/merge/([a-zA-Z0-9_\.\-]+)\.\.\.([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.merge'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/pulls/?$', 'repo.views.pulls'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/pull/new/?$', 'repo.views.pull_new_default'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/pull/new/(\w+):([a-zA-Z0-9_\.\-]+)\.\.\.(\w+):([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.pull_new'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/pull/diff/(\w+):([a-zA-Z0-9_\.\-]+)\.\.(\w+):([a-zA-Z0-9_\.\-]+)/(\d+)/?$', 'repo.views.pull_diff'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/pull/commits/(\w+):([a-zA-Z0-9_\.\-]+)\.\.\.(\w+):([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.pull_commits'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/pull/(\d+)/?$', 'repo.views.pull_show'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/pull/(\d+)/merge/?$', 'repo.views.pull_merge'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/pull/(\d+)/reject/?$', 'repo.views.pull_reject'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/pull/(\d+)/close/?$', 'repo.views.pull_close'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/pulse/?$', 'repo.views.pulse'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/stats/?$', 'repo.views.stats'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/log/graph/([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.log_graph'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/refs/graph/?$', 'repo.views.refs_graph_default'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/refs/graph/([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.refs_graph'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/refs/create/([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.refs_create'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/refs/branch/create/([a-zA-Z0-9_\.\-]+)/([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.refs_branch_create'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/refs/branch/delete/([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.refs_branch_delete'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/refs/tag/create/([a-zA-Z0-9_\.\-]+)/([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.refs_tag_create'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/refs/tag/delete/([a-zA-Z0-9_\.\-]+)/?$', 'repo.views.refs_tag_delete'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/refs/?$', 'repo.views.refs'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/fork/?$', 'repo.views.fork'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/watch/?$', 'repo.views.watch'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/unwatch/?$', 'repo.views.unwatch'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/star/?$', 'repo.views.star'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/unstar/?$', 'repo.views.unstar'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/diff/([a-zA-Z0-9_\.\-]+)\.\.([a-zA-Z0-9_\.\-]+)/(\d+)/([^\@\#\$\&\\\*\"\'\<\>\|\;]*)$', 'repo.views.diff'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/diff/([a-zA-Z0-9_\.\-]+)\.\.([a-zA-Z0-9_\.\-]+)/(\d+)/?', 'repo.views.diff_default'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/member_users/?$', 'repo.views.member_users'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/?$', 'repo.views.settings'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/members/?$', 'repo.views.members'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/member/add/?$', 'repo.views.add_member'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/member/remove/?$', 'repo.views.remove_member'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/hooks/?$', 'repo.views.hooks'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/hook/web_hook_url/add/?$', 'repo.views.add_web_hook_url'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/hook/web_hook_url/(\d+)/enable/?$', 'repo.views.enable_web_hook_url'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/hook/web_hook_url/(\d+)/disable/?$', 'repo.views.disable_web_hook_url'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/hook/web_hook_url/(\d+)/remove/?$', 'repo.views.remove_web_hook_url'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/generate_deploy_url/?$', 'repo.views.generate_deploy_url'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/forbid_dploy_url/?$', 'repo.views.forbid_dploy_url'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/enable_dropbox_sync/?$', 'repo.views.enable_dropbox_sync'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/disable_dropbox_sync/?$', 'repo.views.disable_dropbox_sync'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/settings/delete/?$', 'repo.views.delete'),
    
    # issue
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/issues/?$', 'issue.views.issues'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/issues/(\d+)/?$', 'issue.views.show_default'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/issues/(\d+)/(\d+)/?$', 'issue.views.show'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/issues/create/?$', 'issue.views.create'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/issues/edit/(\d+)/?$', 'issue.views.edit'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/issues/delete/(\d+)/?$', 'issue.views.delete'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/issues/update/(\d+)/(\w+)/?$', 'issue.views.update'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/issues/list/(\w+)/(\d+)/(\d+)/(\d+)/(\w+)/(\d+)/?$', 'issue.views.issues_list'),
    url(r'^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_\-]+)/issues/comment/delete/(\d+)/?$', 'issue.views.comment_delete'),
    
)
handler404 = 'gitshell.help.views.error'
handler500 = 'gitshell.help.views.error'

