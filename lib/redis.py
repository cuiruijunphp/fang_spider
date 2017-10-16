import redis

from lib.cfg import Cfg
from lib.log import Log


class Redis(object):

    conn = None
    _which_redis = None
    _cfg = None

    def __init__(self):
        pass

    @classmethod
    def connect(cls, which_redis='redis_default'):

        if not which_redis:
            raise AttributeError('redis cannot be None')

        if Redis._which_redis and which_redis != Redis._which_redis:
            cls.close()

        Redis._which_redis = which_redis

        if not Redis.conn:
            cfg_parser = Cfg.load()
            if not cfg_parser.has_section(which_redis):
                raise FileNotFoundError('redis conf not found')
            Redis._cfg = dict(cfg_parser.items(which_redis))

            # Connect to the database
            Redis.conn = redis.StrictRedis(host=Redis._cfg['redis_host'], port=Redis._cfg['redis_port'],password=Redis._cfg['redis_pwd'])

        return Redis.conn

    @classmethod
    def close(cls):
        if Redis.conn:
            try:
                #Redis.conn.close()
                Redis.conn = None
                Redis._cfg = None
                Redis._which_redis = None
            except:
                pass

    def __del__(self):
        self.close()
