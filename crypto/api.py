from typing import Callable, Optional
import httpx
from crypto.models.crypto_websocket import CryptoWebsocket
from crypto.models.coin import Coin
from crypto.models.statistic import Statistic
import asyncio
from crypto.models.websocket_details import WebsocketDetails
from crypto.urls import (
    get_token_data_url,
    get_top_100_url,
    format_history_url,
    get_fear_greed_index_url,
)
from crypto.models.types import Top100Coin, HistoryPoint, GreedFearHistoryPoint
import time
from datetime import datetime, timedelta


class RealtimeCryptoTracker:
    def __init__(self):
        self.client = httpx.Client()

    def get_coin(self, coin_name: str) -> Optional[Coin]:
        """
        Get data of a single coin.
        """

        res = self.client.get(get_token_data_url(coin_name))
        res_json = res.json()

        if "data" not in res_json:
            return None

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
        if "data" not in res_json:
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

    def get_fear_greed_index_history(
        self, from_unix: int, to_unix: int
    ) -> list[GreedFearHistoryPoint]:
        """
        Get the greed/fear index history for a given time frame.

        Return example:
        [
            {
                "score": 36.62,
                "name": "Fear",
                "timestamp": "1694131200"
            },
            {
                "score": 32.00,
                "name": "Fear",
                "timestamp": "1694931200"
            }
        ]
        """

        res = self.client.get(get_fear_greed_index_url(from_unix, to_unix))
        res_data = res.json()["data"]
        if "dataList" not in res_data:
            return []

        history_list: list[GreedFearHistoryPoint] = res_data["dataList"]

        return history_list

    def get_current_fear_greed_index(self) -> int:
        """
        Get current fear/greed index.
        """

        # Get yesterday unix
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        yesterday_unix = int(time.mktime(yesterday.timetuple()))

        now_unix = time.time()

        res = self.client.get(
            get_fear_greed_index_url(int(yesterday_unix), int(now_unix))
        )
        res_data = res.json()["data"]
        if "dataList" not in res_data:
            return 0

        score = int(res_data["dataList"][0]["score"])

        return score

    def get_best_performing_cryptos(self, range: str) -> Optional[list]:
        """
        Get best performing cryptos in the top 100.

        range examples: 1h, 24h, 7d, 30d, 60d, 90d, 1y

        Return value is sorted high to low
        """

        valid_ranges = ["1h", "24h", "7d", "30d", "60d", "90d", "1y"]
        if range not in valid_ranges:
            return None

        result = []

        res = self.client.get(get_top_100_url())
        top_100_list = res.json()["data"]

        if range == "24h":
            sortedli = sorted(
                top_100_list, key=lambda d: d["changePercent24Hr"], reverse=True
            )

            return sortedli

        for coin in top_100_list:
            coin_obj = self.get_coin(coin["name"])

            if coin_obj is None:
                continue

            price_change = coin_obj.get_statistics().get_price_change(range)
            if price_change:
                result.append(
                    {"name": coin_obj.get_slug(), "priceChange" + range: price_change}
                )

        return sorted(result, key=lambda d: d["priceChange" + range], reverse=True)


async def main():
    tracker = RealtimeCryptoTracker()
    track_list = [
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
        name = ws_detail.get_crypto()
        print(f"{name}: {new_price}")

    # asyncio.create_task(tracker.realtime_prices(track_list, print_res))
    print(tracker.get_best_performing_cryptos("7d"))
    # print(tracker.get_history("stellar", "1Y"))
    await asyncio.sleep(200000)


if __name__ == "__main__":
    asyncio.run(main())
