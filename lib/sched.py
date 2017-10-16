import re

from lib.redis import Redis


class Sched(object):
    CACHE_KEY_PROXIES = 'JOBS-09781M:crawl:sched'

    def add(self):
        if self.proxy_valid():
           return Redis.connect().zadd(self.CACHE_KEY_PROXIES, 0, self.proxy_str)

    @classmethod
    def del_all(cls):
        return Redis.connect().delete(cls.CACHE_KEY_PROXIES)

    @classmethod
    def all(cls):
        return list(Redis.connect().lrange(cls.CACHE_KEY_PROXIES, 0, -1))

    @classmethod
    def all_valid(cls):
        return list(Redis.connect().zrangebyscore(cls.CACHE_KEY_PROXIES, 0.1, 1000))

    @classmethod
    def count(cls):
        return Redis.connect().llen(cls.CACHE_KEY_PROXIES)

    @classmethod
    def remove_invalid(cls):
        return Redis.connect().zremrangebyscore(cls.CACHE_KEY_PROXIES, -1, 0.1)

    @classmethod
    def remove_values(cls,value):
        return Redis.connect().lrem(cls.CACHE_KEY_PROXIES, 1, value)

    @classmethod
    def incr_score(cls, proxy_str):
        return Redis.connect().zincrby(cls.CACHE_KEY_PROXIES, proxy_str)

    @classmethod
    def update_score(cls, proxy_str):
        return Redis.connect().zadd(cls.CACHE_KEY_PROXIES, 1, proxy_str)


