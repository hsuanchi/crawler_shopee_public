import os
from pydantic import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(BaseSettings):
    PROXY_URL: str

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = basedir + "/crawler_bigquery.json"

    class Config:
        env_file = ".env"


class DevelopmentConfig(BaseConfig):
    pass


class OfficallyConfig(BaseConfig):
    pass


config = {
    "development": DevelopmentConfig,
    "offically": OfficallyConfig,
    "default": OfficallyConfig,
}

settings = config["default"]()
