from config.config import settings
from view.utils import timer
from view.check_ip_pool import CheckIPAddress
from view.api_v4_get_shop_detail import ShopDetailCrawler
from view.api_v4_get_product_detail import ProductDetailCrawler


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
        # self.check_ip_pool()

        # Step 1 > input shop_names > get shop_detail
        crawler_shop_detail = ShopDetailCrawler()
        result_shop_detail = crawler_shop_detail(self.input_shop_names)
        logger.info(
            f"⌲ Step1 Total shop detail fetched: {len(result_shop_detail.index)}"
        )

        # Step 2 > input shop_detail > get product_id
        crawler_product_detail = ProductDetailCrawler()
        result_product_detail = crawler_product_detail(result_shop_detail)
        result_product_detail["user_name"] = self.user_name
        result_product_detail["user_email"] = self.user_email
        logger.info(
            f"⌲ Step2 Total pdp detail fetched: {len(result_product_detail.index)}"
        )

        # Step 3 > combin & claen data > save data to Bigquery
        self.save_to_bigquery(result_shop_detail, result_product_detail)
        logger.info(f"⌲ Step3 Data saved to BigQuery")

    def check_ip_pool(self):
        check_ip = CheckIPAddress()
        check_ip(test_times=5)

    def save_to_bigquery(self, shop_details, product_details):
        client = bq.Client()
        shop_details.to_gbq("shopee.shop_detail", client.project, if_exists="append")
        product_details.to_gbq("shopee.pdp_detail", client.project, if_exists="append")


if __name__ == "__main__":

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
                "join800127",
                "ginilin0982353562",
                "ru8285fg56",
                "wangshutung",
                "taiwan88888",
                "baoshenfg",
                "cyf66666",
                "buddha8888",
                "dragon9168",
                "sinhochen77",
                "jouhsuansu",
            ],
            "input_product_ids": [],
        }
    }

    user_dict = user_dict["a0025071@gmail.com"]
    do = Crawler(user_dict)
    do()
