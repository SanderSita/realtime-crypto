from typing import Callable
import httpx
from crypto.models.crypto_websocket import CryptoWebsocket
from crypto.models.coin import Coin
from crypto.models.statistic import Statistic
import asyncio
from crypto.models.websocket_details import WebsocketDetails
from crypto.urls import get_token_data_url, get_top_100_url, format_history_url
from crypto.models.types import Top100Coin, HistoryPoint


class RealtimeCryptoTracker:
    def __init__(self):
        self.client = httpx.Client()

    def get_coin(self, coin_name: str) -> Coin:
        """
        Get data of a single coin.
        """
        res = self.client.get(get_token_data_url(coin_name))
        json_data = res.json()["data"]

        price_stats = Statistic(**json_data["statistics"])

        id = json_data["id"]
        desc = json_data["description"]
        symbol = json_data["symbol"]

        coin_obj = Coin(id, symbol, coin_name, desc, price_stats)
        return coin_obj

    def get_current_price(self, coin_name: str):
        """
        slug: provide the slug of a coin, for example https://coinmarketcap.com/currencies/bitcoin/ is "bitcoin"
        """
        res = self.client.get(get_token_data_url(coin_name))
        price_json = res.json()

        if price_json["status"]["error_code"] != "0":
            return 0

        price = price_json["data"]["statistics"]["price"]

        return price

    def get_coin_id(self, coin_name: str) -> int:
        """
        Returns the coinmarketcap id of a given crypto
        """
        res = self.client.get(get_token_data_url(coin_name))
        res_json = res.json()
        if not "data" in res_json:
            return 0

        json_data = res.json()["data"]
        id = json_data["id"]
        return int(id)

    async def realtime_prices(self, cryptocurrencies: list[str], callback: Callable):
        """
        Joins the coinmarketcap websocket.
        Get realtime prices through the callback function.
        """
        crypto_ws = CryptoWebsocket(cryptocurrencies, callback)
        await crypto_ws.websocket_init()

    def get_top_100_coins(self) -> list[Top100Coin]:
        """
        Get top 100 crypto on coinmarketcap ranked by marketcap.

        Example output
        {
            'name': 'Bitcoin',
            'symbol': 'BTC',
            'price': '58104.2710616952577758'
            'rank': 1
        }
        """
        res = self.client.get(get_top_100_url())
        cryptocurrencies = res.json()["data"]
        return [
            {
                "name": crypto["name"],
                "symbol": crypto["symbol"],
                "price": crypto["priceUsd"],
                "rank": crypto["rank"],
            }
            for crypto in cryptocurrencies
        ]

    def get_history(self, coin: int | str, range: str) -> list[HistoryPoint]:
        """
        Get the price history for a given.
        Example range inputs: 1h, 1d, 7d, 1m, 3m, 1y

        Return example {'id': '1', 'timestamp': '1723334400', 'price': 60944}
        """
        if isinstance(coin, str):
            coin = self.get_coin_id(coin)
            if not coin:
                return None

        res = self.client.get(format_history_url(coin, range))
        history_json = res.json()

        if history_json["status"]["error_code"] != "0":
            return

        history_data = history_json["data"]["points"]

        return [
            {"id": coin, "timestamp": point, "price": history_data[point]["v"][0]}
            for point in history_data
        ]


async def main():
    tracker = RealtimeCryptoTracker()
    li = [
        "bitcoin",  # BTC
        "ethereum",  # ETH
        "cardano",  # ADA
        "solana",  # SOL
        "ripple",  # XRP
        "polkadot",  # DOT
        "dogecoin",  # DOGE
        "litecoin",  # LTC
        "chainlink",  # LINK
        "avalanche",  # AVAX
        "tron",  # TRX
        "stellar",  # XLM
    ]

    async def print_res(ws_detail: WebsocketDetails):
        new_price = ws_detail.get_new_price()

    # asyncio.create_task(tracker.realtime_prices(li, print_res))
    print(tracker.get_history("gtrgtrgrt", "1Y"))
    # await asyncio.sleep(200000)


if __name__ == "__main__":
    asyncio.run(main())
