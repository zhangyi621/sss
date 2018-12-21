import os
from redis import Redis


def get_pro_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaseConfig(object):
    DEBUG = True
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}/dev.cms.db".format(get_pro_dir())
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Devconfig(BaseConfig):
    # session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = Redis(host="127.0.0.1", port=6390)


class APIConfig(BaseConfig):
    pass


class ProductCongig(object):
    DEBUG = False
