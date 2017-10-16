import re

from lib.redis import Redis


class Proxy(object):
    schema = None
    ip = None
    port = None
    proxy_str = None

    CACHE_KEY_PROXIES = 'crawl:proxies'

    def __init__(self, schema='http://', ip='127.0.0.1', port='80'):
        self.schema = str(schema).strip()
        self.ip = str(ip).strip()
        self.port = str(port).strip()
        self.proxy_str = str(self.schema + self.ip + ':' + self.port)

    def add(self):
        if self.proxy_valid():
           return Redis.connect().zadd(self.CACHE_KEY_PROXIES, 0, self.proxy_str)

    def proxy_valid(self):
        verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"

        if re.findall(verify_regex, self.proxy_str):
            return True

        return False

    @classmethod
    def del_all(cls):
        return Redis.connect().delete(cls.CACHE_KEY_PROXIES)

    @classmethod
    def all(cls):
        return list(Redis.connect().zrange(cls.CACHE_KEY_PROXIES, 0, -1))

    @classmethod
    def all_valid(cls):
        return list(Redis.connect().zrangebyscore(cls.CACHE_KEY_PROXIES, 0.1, 1000))

    @classmethod
    def count(cls):
        return Redis.connect().zcard(cls.CACHE_KEY_PROXIES)

    @classmethod
    def remove_invalid(cls):
        return Redis.connect().zremrangebyscore(cls.CACHE_KEY_PROXIES, -1, 0.1)

    @classmethod
    def incr_score(cls, proxy_str):
        return Redis.connect().zincrby(cls.CACHE_KEY_PROXIES, proxy_str)

    @classmethod
    def update_score(cls, proxy_str):
        return Redis.connect().zadd(cls.CACHE_KEY_PROXIES, 1, proxy_str)


