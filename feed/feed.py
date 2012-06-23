#!/usr/bin/python

import redis
from gitshell import settings


""" feed, sorted sets, random identify hashes keys r, u, wu, bwu, wr, c """
FEED_TYPE = {
    'REPOS' : 'r',
    'PRI_USER' : 'pru',
    'PUB_USER' : 'puu',
    'WATCH_USER' : 'wu',
    'BEWATCH_USER' : 'bwu',
    'WATCH_REPOS' : 'wr',
    'COMM' : 'c',
    'IDENTIFY_CHECK' : 'ic',
}

""" all method about feed and redis """
class FeedAction():
    """ feed aciton by redis """
    def __init__(self):
        self.redis = redis.StrictRedis(
            host = settings.REDIS_HOST,
            port = settings.REDIS_PORT,
            socket_timeout = settings.REDIS_SOCKET_TIMEOUT
        )

    """ all modify method """
    def madd_repos_feed(self, repos_id, sortedset_list):
        key = '%s:%s' % (FEED_TYPE['REPOS'], repos_id)
        self.redis.zadd(key, *tuple(sortedset_list))
        self.redis.zremrangebyrank(key, 100, 200)

    def madd_pri_user_feed(self, user_id, sortedset_list):
        key = '%s:%s' % (FEED_TYPE['PRI_USER'], user_id)
        self.redis.zadd(key, *tuple(sortedset_list))
        self.redis.zremrangebyrank(key, 100, 200)

    def madd_pub_user_feed(self, user_id, sortedset_list):
        key = '%s:%s' % (FEED_TYPE['PUB_USER'], user_id)
        self.redis.zadd(key, *tuple(sortedset_list))
        self.redis.zremrangebyrank(key, 100, 200)

    def add_repos_feed(self, repos_id, timestamp, feed_id):
        self.madd_repos_feed(repos_id, [-timestamp, feed_id])

    def add_pri_user_feed(self, user_id, timestamp, feed_id):
        self.madd_pri_user_feed(user_id, [-timestamp, feed_id])

    def add_pub_user_feed(self, user_id, timestamp, feed_id):
        self.madd_pub_user_feed(user_id, [-timestamp, feed_id])

    def add_watch_user(self, user_id, timestamp, watch_user_id):
        key = '%s:%s' % (FEED_TYPE['WATCH_USER'], user_id)
        self.redis.zadd(key, -timestamp, watch_user_id)
        self.redis.zremrangebyrank(key, 100, 200)

    def remove_watch_user(self, user_id, watch_user_id):
        key = '%s:%s' % (FEED_TYPE['WATCH_USER'], user_id)
        self.redis.zrem(key, watch_user_id)

    def add_bewatch_user(self, user_id, timestamp, bewatch_user_id):
        key = '%s:%s' % (FEED_TYPE['BEWATCH_USER'], user_id)
        self.redis.zadd(key, -timestamp, bewatch_user_id)
        self.redis.zremrangebyrank(key, 20, 200)

    def remove_bewatch_user(self, user_id, bewatch_user_id):
        key = '%s:%s' % (FEED_TYPE['BEWATCH_USER'], user_id)
        self.redis.zrem(key, bewatch_user_id)

    def add_watch_repos(self, user_id, timestamp, watch_repos_id):
        key = '%s:%s' % (FEED_TYPE['WATCH_REPOS'], user_id)
        self.redis.zadd(key, -timestamp, watch_repos_id)
        self.redis.zremrangebyrank(key, 100, 200)

    def remove_watch_repos(self, user_id, watch_repos_id):
        key = '%s:%s' % (FEED_TYPE['WATCH_REPOS'], user_id)
        self.redis.zrem(key, watch_repos_id)

    def add_comm_feed(self, user_id, timestamp, feed_id):
        key = '%s:%s' % (FEED_TYPE['COMM'], user_id)
        self.redis.zadd(key, -timestamp, feed_id)
        self.redis.zremrangebyrank(key, 100, 200)

    def remove_comm_feed(self, user_id, feed_id):
        key = '%s:%s' % (FEED_TYPE['COMM'], user_id)
        self.redis.zrem(key, feed_id)

    """ all get method """
    def get_repos_feeds(self, repos_id, start, num_items):
        key = '%s:%s' % (FEED_TYPE['REPOS'], repos_id)
        return self.redis.zrange(key, start, num_items, withscores=True)

    def get_pri_user_feeds(self, user_id, start, num_items):
        key = '%s:%s' % (FEED_TYPE['PRI_USER'], user_id)
        return self.redis.zrange(key, start, num_items, withscores=True)

    def get_pub_user_feeds(self, user_id, start, num_items):
        key = '%s:%s' % (FEED_TYPE['PUB_USER'], user_id)
        return self.redis.zrange(key, start, num_items, withscores=True)

    def get_watch_users(self, user_id, start, num_items):
        key = '%s:%s' % (FEED_TYPE['WATCH_USER'], user_id)
        return self.redis.zrange(key, start, num_items, withscores=True)

    def get_bewatch_users(self, user_id, start, num_items):
        key = '%s:%s' % (FEED_TYPE['BEWATCH_USER'], user_id)
        return self.redis.zrange(key, start, num_items, withscores=True)

    def get_watch_reposes(self, user_id, start, num_items):
        key = '%s:%s' % (FEED_TYPE['WATCH_REPOS'], user_id)
        return self.redis.zrange(key, start, num_items, withscores=True)

    def get_comm_feeds(self, user_id, start, num_items):
        key = '%s:%s' % (FEED_TYPE['COMM'], user_id)
        return self.redis.zrange(key, start, num_items, withscores=True)

if __name__ == '__main__':
    feedAction = FeedAction()
    print feedAction.get_pri_user_feeds(1, 0, -1)