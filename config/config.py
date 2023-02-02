import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

from pydantic import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(BaseSettings):
    PROXY_URL: str
    ENV: str = "default"

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = basedir + "/crawler_bigquery.json"

    class Config:
        env_file = ".env"


class DevelopmentConfig(BaseConfig):
    def setup_logging(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
            handlers=[
                logging.StreamHandler(),
                RotatingFileHandler(
                    datetime.now().strftime("./log/dev_shopee_%Y-%m-%d.log"),
                    maxBytes=1000000,
                    backupCount=1,
                ),
            ],
        )


class OfficallyConfig(BaseConfig):
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
            handlers=[
                logging.StreamHandler(),
                RotatingFileHandler(
                    datetime.now().strftime("./log/live_shopee_%Y-%m-%d.log"),
                    maxBytes=1000000,
                    backupCount=1,
                ),
            ],
        )


config = {
    "development": DevelopmentConfig,
    "offically": OfficallyConfig,
    "default": OfficallyConfig,
}
settings = config[BaseConfig().ENV]()
settings.setup_logging()
