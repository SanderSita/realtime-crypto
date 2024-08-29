from typing import Callable
import httpx
from crypto.models.crypto_websocket import CryptoWebsocket
from urls import urls
from crypto.models.coin import Coin
from crypto.models.statistic import Statistic
import json
import asyncio


class RealtimeCrypto:
    def __init__(self):
        self.client = httpx.Client()

    def get_coin(self, slug: str) -> Coin:
        res = self.client.get(urls["token_data"] + slug)
        json_data = res.json()["data"]

        price_stats = Statistic(**json_data["statistics"])

        id = json_data["id"]
        desc = json_data["description"]
        symbol = json_data["symbol"]

        coin_obj = Coin(id, symbol, slug, desc, price_stats)
        return coin_obj

    def get_current_price(self, crypto_name: str):
        """
        slug: provide the slug of a coin, for example https://coinmarketcap.com/currencies/bitcoin/ is "bitcoin"
        """
        res = self.client.get(urls["token_data"] + crypto_name)
        price_json = res.json()

        if price_json["status"]["error_code"] != "0":
            return 0

        price = price_json["data"]["statistics"]["price"]
        print(type(price))
        print(price)
        return price

    @classmethod
    def get_coin_id(self, coin_name: str) -> int:
        res = self.client.get(urls["token_data"] + coin_name)
        json_data = res.json()["data"]
        id = json_data["id"]
        return int(id)

    async def realtime_prices(self, crypto_names: list[str], callback: Callable):
        crypto_ws = CryptoWebsocket(crypto_names, callback)
        await crypto_ws.websocket_init()

    def get_top_100_coins(self):
        pass


async def main():
    realtime_crypto = RealtimeCrypto()
    li = ["bitcoin"]

    def print_res(res):
        print(res)

    asyncio.create_task(realtime_crypto.realtime_prices(li, print_res))

    print("HEREEEE")
    await asyncio.sleep(200000)


if __name__ == "__main__":
    asyncio.run(main())
