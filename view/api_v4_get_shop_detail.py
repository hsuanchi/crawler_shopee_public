from config.config import settings
from view.utils import timer

import os
import json
import logging
import asyncio
import datetime

import aiohttp
import pandas as pd
from pydantic import BaseModel

logger = logging.getLogger()


class ShopParams(BaseModel):
    shop_created: str
    shopid: int
    shop_name: str
    username: str
    follower_count: int
    has_decoration: bool
    item_count: int
    response_rate: int
    campaign_hot_deal_discount_min: int
    description: str
    rating_star: float
    shop_rating_good: int
    shop_rating_bad: int
    shop_rating_normal: int


class CrawlerShopDetail:
    def __init__(self):
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.shop_detail_api = "https://shopee.tw/api/v4/shop/get_shop_base?entry_point=ShopByPDP&need_cancel_rate=true&request_source=shop_home_page&version=1&username="
        self.shop_detail = []

    @timer
    def __call__(self, input_shop_names):
        async def parser_shop_html(html):
            shop = json.loads(html)["data"]
            print(shop["name"])

            dateArray = datetime.datetime.utcfromtimestamp(shop["ctime"])
            transfor_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")

            shop_info = ShopParams(
                shop_created=transfor_time,
                shopid=shop["shopid"],
                shop_name=shop["name"],
                username=shop["account"]["username"],
                follower_count=shop["follower_count"],
                has_decoration=shop["has_decoration"],
                item_count=shop["item_count"],
                response_rate=shop["response_rate"],
                campaign_hot_deal_discount_min=shop["campaign_hot_deal_discount_min"],
                description=shop["description"],
                rating_star=shop["rating_star"],
                shop_rating_good=shop["shop_rating"]["rating_good"],
                shop_rating_bad=shop["shop_rating"]["rating_bad"],
                shop_rating_normal=shop["shop_rating"]["rating_normal"],
            )
            self.shop_detail.append(shop_info.dict())

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
                logger.warning(f"Exception: {e}")

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

        df = pd.DataFrame(self.shop_detail)
        print(df)
        df.to_csv(self.basepath + "/csv/shop_detail.csv", index=False)
        return df


if __name__ == "__main__":
    """
    api example
    https://shopee.tw/api/v4/shop/get_shop_base?entry_point=ShopByPDP&need_cancel_rate=true&request_source=shop_home_page&username=mhw3bombertw&version=1
    """
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
