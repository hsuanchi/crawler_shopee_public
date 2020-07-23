import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:  # 基本配置
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = basedir + "/Crawler-Bigquery.json"


class DevelopmentConfig(BaseConfig):
    pass


class OfficallyConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'offically': OfficallyConfig,
    'default': DevelopmentConfig
}
