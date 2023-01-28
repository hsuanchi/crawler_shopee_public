import os
import json
import time
import asyncio
import datetime

import aiohttp
import pandas as pd

from config.config import settings


class CrawlerShopDetail:
    def __init__(self):
        self.basepath = os.path.abspath(os.path.dirname(__file__))

        self.shop_detail_api = "https://shopee.tw/api/v4/shop/get_shop_base?entry_point=ShopByPDP&need_cancel_rate=true&request_source=shop_home_page&version=1&username="
        self.shop_detail_dict = {
            "shop_name": [],  # 商家名稱
            "shopid": [],  # 商家id
            "shop_ctime": [],  # 加入時間
            "shop_country": [],  # 國家
            "shop_item_count": [],  # 商品數
            "shop_place": [],  # 地址
            "shop_rating_star": [],  # 平均評分
            "shop_rating_bad": [],
            "shop_rating_normal": [],
            "shop_rating_good": [],
        }

    def __call__(self, input_shop_names):
        async def parser_shop_html(html):
            shop = json.loads(html)
            print(shop["data"]["name"])
            # dateArray = datetime.datetime.utcfromtimestamp(shop["data"]["ctime"])
            # transfor_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
            # self.shop_detail_dict["shop_ctime"].append(transfor_time)
            # self.shop_detail_dict["shopid"].append(shop["data"]["shopid"])
            # self.shop_detail_dict["shop_name"].append(shop["data"]["name"])
            # self.shop_detail_dict["shop_country"].append(shop["data"]["country"])
            # self.shop_detail_dict["shop_item_count"].append(shop["data"]["item_count"])
            # self.shop_detail_dict["shop_place"].append(shop["data"]["place"])
            # self.shop_detail_dict["shop_rating_star"].append(
            #     shop["data"]["rating_star"]
            # )
            # self.shop_detail_dict["shop_rating_bad"].append(shop["data"]["rating_bad"])
            # self.shop_detail_dict["shop_rating_normal"].append(
            #     shop["data"]["rating_normal"]
            # )
            # self.shop_detail_dict["shop_rating_good"].append(
            #     shop["data"]["rating_good"]
            # )

        async def get_shop_detail(client, query_url):
            try:
                async with client.get(
                    query_url,
                    proxy=settings.PROXY_URL,
                ) as response:
                    html = await response.text()
                    assert response.status == 200
                    await parser_shop_html(html)
            except Exception as e:
                print("---Exception---:", e)

        async def main(crawler_shop_urls):
            headers = {
                "User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
                "referer": "https://shopee.tw/",
                "X-Requested-With": "XMLHttpRequest",
            }
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False, limit=100),
                headers=headers,
            ) as client:
                tasks = [
                    get_shop_detail(client, query_url)
                    for query_url in crawler_shop_urls
                ]
                await asyncio.gather(*tasks)

        crawler_shop_urls = []
        for id in range(len(input_shop_names)):
            crawler_shop_urls.append(self.shop_detail_api + str(input_shop_names[id]))
        asyncio.run(main(crawler_shop_urls))

        # df = pd.DataFrame(self.shop_detail_dict)
        # df.to_csv(self.basepath + "/csv/shop_detail.csv", index=False)
        # return df
        return "666"


if __name__ == "__main__":
    # // api example
    # https://shopee.tw/api/v4/shop/get_shop_base?entry_point=ShopByPDP&need_cancel_rate=true&request_source=shop_home_page&username=mhw3bombertw&version=1

    time_start = time.time()

    input_shop_names = [
        "fulinxuan",
        # "pat6116xx",
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
        # "s0985881631",
        # "jouhsuansu",
    ]

    do = CrawlerShopDetail()
    result = do(input_shop_names)

    print(result)
    print(time.time() - time_start)
