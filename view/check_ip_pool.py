from config.config import settings


import os
import time
import asyncio

import aiohttp


class CheckIPAddress:
    def __init__(self):
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.ip_pool_api = "https://ipv4.webshare.io/"

    def __call__(self, test_times=5):
        async def get_ip_detail(client, query_url):
            try:
                async with client.get(
                    query_url,
                    proxy=settings.PROXY_URL,
                ) as response:
                    html = await response.text()
                    assert response.status == 200
                    print(html)
            except Exception as e:
                print("---Exception---:", e)

        async def main(crawler_urls):
            headers = {
                "User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
                "X-Requested-With": "XMLHttpRequest",
            }
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False, limit=100),
                headers=headers,
            ) as client:
                tasks = [get_ip_detail(client, query_url) for query_url in crawler_urls]
                await asyncio.gather(*tasks)

        crawler_urls = []
        for id in range(test_times):
            crawler_urls.append(self.ip_pool_api)
        asyncio.run(main(crawler_urls))

        return "666"


if __name__ == "__main__":

    # // api example
    # https://ipv4.webshare.io/

    time_start = time.time()

    do = CheckIPAddress()
    do(test_times=5)

    print(time.time() - time_start)
