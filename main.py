from view.get_shop_detail import Crawler_shop_detail
from view.get_product_url import Crawler_product_id
from view.get_product_detail import Crawler_product_detail

# from view.clean_data import run_clean

# from config.config import config
# from google.cloud import bigquery as bq

import time
import datetime
import pandas as pd

now = lambda: datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")


class Crawler:
    def __init__(self, user_dict):
        # 連線 bigqeury
        # self.client = bq.Client()

        # init
        self.input_shop_ids = user_dict["input_shop_ids"]
        self.user_email = user_dict["user_info"]["Email"]
        self.user_name = user_dict["user_info"]["Name"]

    def __call__(self):
        # Step 1 > input shop_id > get shop_detail
        crawler_shop_detail = Crawler_shop_detail()
        result_shop_detail = crawler_shop_detail(self.input_shop_ids)
        print(now(), "step1_爬取商家數量：", len(result_shop_detail.index))

        # Step 2 > input shop_detail > get product_id
        crawler_product_id = Crawler_product_id()
        result_product_id = crawler_product_id(result_shop_detail)
        print(now(), "step2_爬取商家產品數：", len(result_product_id.index))

        # Step 3 > input product_id > get product_detail
        crawler_product_detail = Crawler_product_detail()
        result_product_detail = crawler_product_detail(result_product_id)
        print(now(), "step3_爬取產品細節：", len(result_product_detail.index))

        # Step 4 > combin & claen data > save data to Bigquery
        df = pd.merge(
            result_product_detail, result_shop_detail, on=["shopid"], how="outer"
        )

        df["hashtag_list"] = df["hashtag_list"].astype(str)
        df["time_stamp"] = df["time_stamp"].astype(str)
        df["user_Name"] = self.user_name
        df["user_Email"] = self.user_email
        print(now(), "step4_清理資料 & 存入：", len(df.index))

        # To bigquery
        # table = self.client.dataset('crawler_product_detail').table('data')
        # job = self.client.load_table_from_dataframe(df, table)
        # job.result()


if __name__ == "__main__":

    # 填入 User 和爬取 Shop ID
    user_dict = {
        "a0025071@gmail.com": {
            "user_info": {
                "Email": "a0025071@gmail.com",
                "Name": "Max",
            },
            "input_shop_ids": [
                5547415,
                22189057,
                1517097,
                3323966,
                1971812,
                8016627,
                80078149,
                7314701,
                151143321,
                47924061,
                29951329,
                9532352,
                15659558,
                31945247,
                2678128,
                46474821,
                4287756,
            ],
            "input_product_ids": [],
        }
    }

    # 載入 Bigquery
    # config["development"]
    time_start = time.time()

    user_dict = user_dict["a0025071@gmail.com"]
    do = Crawler(user_dict)
    do()

    print(time.time() - time_start)
