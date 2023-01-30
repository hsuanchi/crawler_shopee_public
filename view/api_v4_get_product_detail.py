from view.utils import timer

import os
import json
import logging
import asyncio
import datetime

import aiohttp
import pandas as pd

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ItemParams(BaseModel):
    itemid: str
    shopid: int
    name: str
    currency: str
    stock: int
    status: int
    ctime: int
    t_ctime: str
    sold: int
    historical_sold: int
    liked_count: int
    brand: str
    cmt_count: int
    item_status: str
    price: int
    price_min: int
    price_max: int
    price_before_discount: int
    show_discount: int
    raw_discount: int
    tier_variations_option: str
    rating_star_avg: int
    rating_star_1: int
    rating_star_2: int
    rating_star_3: int
    rating_star_4: int
    rating_star_5: int
    item_type: int
    is_adult: bool
    has_lowest_price_guarantee: bool
    is_official_shop: bool
    is_cc_installment_payment_eligible: bool
    is_non_cc_installment_payment_eligible: bool
    is_preferred_plus_seller: bool
    is_mart: bool
    is_on_flash_sale: bool
    is_service_by_shopee: bool
    shopee_verified: bool
    show_official_shop_label: bool
    show_shopee_verified_label: bool
    show_official_shop_label_in_title: bool
    show_free_shipping: bool

    class Config:
        allow_extra = False


class CrawlerProductDetail:
    def __init__(self):
        self.basepath = os.path.abspath(os.path.dirname(__file__))

        self.search_item_api = "https://shopee.tw/api/v4/shop/search_items"
        self.items_info = []

    @timer
    def __call__(self, shop_detail):
        async def parser_shop_html(html):
            info = json.loads(html)

            if info["total_count"] != 0:
                for item in info["items"]:
                    item = item["item_basic"]

                    dateArray = datetime.datetime.utcfromtimestamp(item["ctime"])
                    transfor_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")

                    item_info = ItemParams(
                        **item,
                        t_ctime=transfor_time,
                        rating_star_avg=item["item_rating"]["rating_star"],
                        rating_star_1=item["item_rating"]["rating_count"][1],
                        rating_star_2=item["item_rating"]["rating_count"][2],
                        rating_star_3=item["item_rating"]["rating_count"][3],
                        rating_star_4=item["item_rating"]["rating_count"][4],
                        rating_star_5=item["item_rating"]["rating_count"][5],
                        tier_variations_option=",".join(
                            item["tier_variations"][0]["options"]
                        )
                        if item.get("tier_variations")
                        else "",
                    )
                    self.items_info.append(item_info.dict())

        async def get_item_detail(client, query_url):
            try:
                async with client.get(query_url) as response:
                    html = await response.text()
                    assert response.status == 200
                    await parser_shop_html(html)
            except Exception as e:
                logger.warning(f"Exception: {e}")

        async def main(crawler_itme_urls):
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
                    get_item_detail(client, query_url)
                    for query_url in crawler_itme_urls
                ]
                await asyncio.gather(*tasks)

        crawler_itme_urls = []

        df_header = pd.DataFrame(
            columns=[field.name for field in ItemParams.__fields__.values()]
        )
        df_header.to_csv(self.basepath + "/csv/pdp_detail.csv", index=False)

        for row in shop_detail.itertuples():

            shop_id = row.shopid
            shop_product_count = row.item_count
            num = 0
            while num < shop_product_count:
                crawler_itme_urls.append(
                    f"{self.search_item_api}?offset={str(num)}&limit=100&order=desc&filter_sold_out=3&use_case=1&sort_by=sales&order=sales&shopid={shop_id}"
                )
                num += 100
            asyncio.run(main(crawler_itme_urls))

            df = pd.DataFrame(self.items_info)
            df.to_csv(
                self.basepath + "/csv/pdp_detail.csv",
                index=False,
                mode="a",
                header=False,
            )
        total_df = pd.read_csv(self.basepath + "/csv/pdp_detail.csv")
        return total_df


if __name__ == "__main__":
    """
    # api example
    # https://shopee.tw/api/v4/shop/search_items?filter_sold_out=1&limit=100&offset=1&order=desc&shopid=5547415&sort_by=pop&use_case=1

    params use_case:
    1: Top Product
    2: ?
    3: ?
    4: Sold out items

    params filter_sold_out:
    1: = sold_out
    2: != sold_out
    3: both

    """

    basepath = os.path.abspath(os.path.dirname(__file__))
    shop_detail = pd.read_csv(basepath + "/csv/shop_detail.csv")
    crawler_product_detail = CrawlerProductDetail()
    result_product_detail = crawler_product_detail(shop_detail)
