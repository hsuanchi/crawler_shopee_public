from config.config import settings
from view.utils import timer
from view.check_ip_pool import CheckIPAddress
from view.api_v4_get_shop_detail import CrawlerShopDetail
from view.api_v4_get_product_detail import CrawlerProductDetail


import logging
import pandas as pd
from google.cloud import bigquery as bq

logger = logging.getLogger(__name__)


class Crawler:
    def __init__(self, user_dict):
        self.input_shop_names = user_dict["input_shop_names"]
        self.user_email = user_dict["user_info"]["Email"]
        self.user_name = user_dict["user_info"]["Name"]

    @timer
    def __call__(self):
        # # Step 0 > check ip pool as expected (This step is not necessary.)
        # check_ip = CheckIPAddress()
        # check_ip(test_times=5)

        # Step 1 > input shop_names > get shop_detail
        crawler_shop_detail = CrawlerShopDetail()
        result_shop_detail = crawler_shop_detail(self.input_shop_names)
        logger.info(f"Step1 總共爬取商家數量: {len(result_shop_detail.index)}")

        # Step 2 > input shop_detail > get product_id
        crawler_product_detail = CrawlerProductDetail()
        result_product_detail = crawler_product_detail(result_shop_detail)
        result_product_detail["user_name"] = self.user_name
        result_product_detail["user_email"] = self.user_email
        logger.info(f"Step2 總共爬取產品細節: {len(result_product_detail.index)}")

        # Step 3 > combin & claen data > save data to Bigquery
        client = bq.Client()
        result_shop_detail.to_gbq(
            "shopee.shop_detail", client.project, if_exists="replace"
        )
        result_product_detail.to_gbq(
            "shopee.pdp_detail", client.project, if_exists="replace"
        )
        logger.info(f"Step3 清理資料 & 存入: {len(result_product_detail.index)}")


if __name__ == "__main__":
    """
    # TODO: add env export
    # TODO: add docker & deploy
    # TODO: add clean.sql
    # TODO: add merge table
    # TODO: add dashboard
    """

    # Insert your email and the shop names you want to crawl
    user_dict = {
        "a0025071@gmail.com": {
            "user_info": {
                "Email": "a0025071@gmail.com",
                "Name": "Max",
            },
            "input_shop_names": [
                "fulinxuan",
                "pat6116xx",
                # "join800127",
                # "ginilin0982353562",
                # "ru8285fg56",
                # "wangshutung",
                # "taiwan88888",
                # "cyf66666",
                # "buddha8888",
                # "dragon9168",
                # "sinhochen77",
                # "baoshenfg",
                # "jouhsuansu",
            ],
            "input_product_ids": [],
        }
    }

    user_dict = user_dict["a0025071@gmail.com"]
    do = Crawler(user_dict)
    do()
