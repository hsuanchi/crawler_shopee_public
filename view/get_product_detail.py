import os
import json
import time
import asyncio
import datetime

import aiohttp
import async_timeout
import pandas as pd


class Crawler_product_detail:
    def __init__(self, max_fail_time=10, max_tasks=30):
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.max_fail_time = max_fail_time
        self.max_tasks = max_tasks

        self.items_dict = {
            "shopid": [],
            "shop_location": [],
            "hashtag_list": [],
            "show_free_shipping": [],
            "name": [],
            "description": [],
            "itemid": [],
            "type_name": [],
            "type_price": [],
            "type_normal_stock": [],
            "type_sold": [],
            "type_stock": [],
            "time_stamp": [],
        }

    def __call__(self, result_product_id):
        async def parser_product_detail_html(html):

            products = json.loads(html)
            item = products["item"]
            items_type = products["item"]["models"]
            now = datetime.datetime.now().strftime("%Y-%m-%d")

            for i in range(len(items_type)):
                self.items_dict["shopid"].append(item["shopid"])
                self.items_dict["shop_location"].append(item["shop_location"])
                self.items_dict["show_free_shipping"].append(item["show_free_shipping"])
                self.items_dict["hashtag_list"].append(item["hashtag_list"])
                self.items_dict["name"].append(item["name"])
                self.items_dict["description"].append(item["description"])
                self.items_dict["itemid"].append(items_type[i]["itemid"])
                self.items_dict["type_name"].append(items_type[i]["name"])
                self.items_dict["type_price"].append(items_type[i]["price"] / 100000)
                self.items_dict["type_normal_stock"].append(
                    items_type[i]["normal_stock"]
                )
                self.items_dict["type_sold"].append(items_type[i]["sold"])
                self.items_dict["type_stock"].append(items_type[i]["stock"])
                self.items_dict["time_stamp"].append(now)
                print(
                    f'已經爬取 {item["shopid"]} ,{item["name"]} , {items_type[i]["name"]}'
                )

        async def fetch_coroutine(client, url, semaphore, fail_time=None):
            try:
                async with semaphore:
                    with async_timeout.timeout(10):
                        async with client.get(url) as response:
                            html = await response.text()
                            assert response.status == 200
                            await parser_product_detail_html(html)

                        return await response.release()
            except Exception as e:
                if fail_time is None:
                    fail_time = 0
                print("fail--------------", e, url, fail_time)
                self.q.put_nowait((url, fail_time))

        async def fetch_fail_coroutine(client, semaphore):
            try:
                while True:
                    url, fail_time = await self.q.get()

                    # 判斷失敗次數
                    if fail_time > self.max_fail_time:
                        self.q.task_done()
                        break
                    fail_time += 1
                    await fetch_coroutine(client, url, semaphore, fail_time)
                    print(url, fail_time)
                    self.q.task_done()

            except asyncio.CancelledError:
                pass
            except Exception as e:
                print("66666", e)

        async def main():

            self.q = asyncio.Queue()  # 存放 fail 的 url
            urls = result_product_id["url"].values.tolist()

            headers = {"User-Agent": "Googlebot"}
            semaphore = asyncio.Semaphore(self.max_tasks)
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False),
                headers=headers,
            ) as client:
                tasks = [fetch_coroutine(client, url, semaphore) for url in urls]
                await asyncio.gather(*tasks)

                tasks_fail = [
                    asyncio.create_task(fetch_fail_coroutine(client, semaphore))
                    for _ in range(self.max_tasks)
                ]

                await self.q.join()
                for task in tasks_fail:
                    task.cancel()

        asyncio.run(main())
        df = pd.DataFrame(self.items_dict)

        df.to_csv(self.basepath + "/csv/product_detail.csv", index=False)

        return df


if __name__ == "__main__":
    time_start = time.time()

    basepath = os.path.abspath(os.path.dirname(__file__))
    result_product_id = pd.read_csv(basepath + "/csv/product_id.csv")

    crawler_product_detail = Crawler_product_detail()
    result_product_detail = crawler_product_detail(result_product_id)
    print(len(result_product_detail))
    print(time.time() - time_start)
