import os
import time
import json
import asyncio

import aiohttp
import pandas as pd


class CrawlerProductId:
    def __init__(self):
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.product_id_api = "https://shopee.tw/api/v2/search_items/?by=price&order=asc&page_type=shop&version=2&limit=100"

        self.product_id_dict = {
            "shopid": [],  # 商家id
            "itemid": [],  # 產品id
        }

    def __call__(self, df):
        async def parser_product_id_html(html):
            product_detail = json.loads(html)
            print(product_detail)
            for i in range(len(product_detail["items"])):
                self.product_id_dict["shopid"].append(
                    product_detail["items"][i]["shopid"]
                )
                self.product_id_dict["itemid"].append(
                    product_detail["items"][i]["itemid"]
                )

        async def get_product_id(client, query_url):
            try:
                async with client.get(query_url) as response:
                    print(query_url)
                    html = await response.text()
                    assert response.status == 200
                    await parser_product_id_html(html)
            except Exception as e:
                print("---Exception---:", e)

        async def main(crawler_product_urls):
            headers = {
                "User-Agent": "Googlebot",
                "Referer": "https://shopee.tw/shop/22189057/search",
                "X-Requested-With": "XMLHttpRequest",
            }
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False, limit=100),
                headers=headers,
            ) as client:
                tasks = [
                    get_product_id(client, query_url)
                    for query_url in crawler_product_urls
                ]
                await asyncio.gather(*tasks)

        crawler_product_urls = []

        shop_ids = df["shopid"].values.tolist()
        shop_items = df["shop_item_count"].values.tolist()

        for i in range(len(shop_ids)):
            num = 0
            while num < shop_items[i]:
                crawler_product_urls.append(
                    self.product_id_api
                    + "&match_id="
                    + str(shop_ids[i])
                    + "&newest="
                    + str(num)
                )
                num += 100
        asyncio.run(main(crawler_product_urls))

        df = pd.DataFrame(self.product_id_dict)

        df["url"] = (
            "https://shopee.tw/api/v2/item/get?itemid="
            + df["itemid"].astype(str)
            + "&shopid="
            + df["shopid"].astype(str)
        )

        df.to_csv(self.basepath + "/csv/product_id.csv", index=False)
        return df


if __name__ == "__main__":
    # // api example
    # https://shopee.tw/api/v2/search_items/?by=price&order=asc&page_type=shop&version=2&limit=30&newest=0&match_id=31945247

    time_start = time.time()

    basepath = os.path.abspath(os.path.dirname(__file__))
    result_shop_detail = pd.read_csv(basepath + "/csv/shop_detail.csv")

    crawler_product_id = CrawlerProductId()
    result_product_id = crawler_product_id(result_shop_detail)

    print(len(result_product_id.index))
    print(time.time() - time_start)
