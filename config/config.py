import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

from pydantic import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(BaseSettings):
    PROXY_URL: str

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = basedir + "/crawler_bigquery.json"

    class Config:
        env_file = ".env"


class DevelopmentConfig(BaseConfig):
    log_file_name = datetime.now().strftime("./log/dev_shopee_%Y-%m-%d.log")


class OfficallyConfig(BaseConfig):
    log_file_name = datetime.now().strftime("./log/live_shopee_%Y-%m-%d.log")


config = {
    "development": DevelopmentConfig,
    "offically": OfficallyConfig,
    "default": OfficallyConfig,
}

settings = config["default"]()

handler = RotatingFileHandler(
    settings.log_file_name,
    maxBytes=1000000,
    backupCount=1,
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    handlers=[handler],
)
