from config.config import settings
from view.utils import timer


import os
import logging
import asyncio

import aiohttp

logger = logging.getLogger(__name__)


class CheckIPAddress:
    def __init__(self):
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.ip_pool_api = "https://ipv4.webshare.io/"

    @timer
    def __call__(self, test_times=5):
        async def get_ip_detail(client, query_url):
            try:
                async with client.get(
                    query_url,
                    proxy=settings.PROXY_URL,
                ) as response:
                    html = await response.text()
                    assert response.status == 200
                    logger.info(f"└── IP: {html}")
            except Exception as e:
                logger.warning(f"Exception: {e}")

        async def main(crawler_urls):
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
            }
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False, limit=100),
                headers=headers,
            ) as client:
                tasks = [get_ip_detail(client, query_url) for query_url in crawler_urls]
                await asyncio.gather(*tasks)

        crawler_urls = []
        for _ in range(test_times):
            crawler_urls.append(self.ip_pool_api)
        asyncio.run(main(crawler_urls))

        return "666"


if __name__ == "__main__":

    # // api example
    # https://ipv4.webshare.io/

    do = CheckIPAddress()
    do(test_times=5)
