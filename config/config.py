import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

from pydantic import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(BaseSettings):
    PROXY_URL: str = None
    ENV: str = "default"

    class Config:
        env_file = ".env"


class ProductionConfig(BaseConfig):
    """
    with sets up logging.INFO and BigQuery
    """

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

    def setup_bigquery(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
            basedir + "/crawler_bigquery.json"
        )

        from google.cloud import bigquery

        client = bigquery.Client()
        return client


class DebugConfig(BaseConfig):
    """
    with log level set to logging.DEBUG
    """

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


class StagingConfig(BaseConfig):
    """
    with log level set to logging.INFO
    """

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
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


config = {
    "dev": DebugConfig,  # log with DEBUG
    "staging": StagingConfig,  # Run without BigQuery
    "prod": ProductionConfig,  # Run with BigQuery
    "default": StagingConfig,
}
settings = config[BaseConfig().ENV]()
settings.setup_logging()
