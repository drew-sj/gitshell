from django.db import models
from gitshell.objectscache.da import query, queryraw, execute, count

class Repos(models.Model):
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, auto_now_add=True, null=False)
    visibly = models.SmallIntegerField(default=0, null=False)

    user_id = models.IntegerField()
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=512, default='')
    lang = models.CharField(max_length=16)
    auth_type = models.SmallIntegerField(default=0)
    quote = models.BigIntegerField(default=0)

    commit = models.IntegerField(default=0)
    watch = models.IntegerField(default=0)
    fork = models.IntegerField(default=0)
    member = models.IntegerField(default=0)

class ReposMember(models.Model):
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, auto_now_add=True, null=False)
    visibly = models.SmallIntegerField(default=0, null=False)

    user_id = models.IntegerField()
    permission = models.SmallIntegerField(default=0)

# commit history from git
# class commit_history(models.Model):

class WatchHistory(models.Model):
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, auto_now_add=True, null=False)
    visibly = models.SmallIntegerField(default=0, null=False)

    repos_id = models.IntegerField()
    user_id = models.IntegerField()

class ForkHistory(models.Model):
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, auto_now_add=True, null=False)
    visibly = models.SmallIntegerField(default=0, null=False)

    repos_id = models.IntegerField()
    fork_repos_id = models.IntegerField()

class ReposManager():

    @classmethod
    def list_repos_by_userId(self, user_id, offset, row_count):
        reposes = query(Repos, 'repos_repos', user_id, 'repos_l_userId', [user_id, offset, row_count])
        return list(reposes)

    @classmethod
    def get_repos_by_userId_id(self, user_id, rid):
        pass

    @classmethod
    def get_repos_by_userId_name(self, user_id, name):
        reposes = query(Repos, 'repos_repos', user_id, 'repos_s_userId_name', [user_id, name])
        if len(list(reposes)) > 0:
            return reposes[0]
        return None

    @classmethod
    def count_repos_by_userId(self, user_id):
        pass

