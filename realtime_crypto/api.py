from typing import Callable, Optional
import httpx
from realtime_crypto.models.crypto_websocket import CryptoWebsocket
from realtime_crypto.models.coin import Coin
from realtime_crypto.models.statistic import Statistic
from realtime_crypto.urls import (
    get_token_data_url,
    get_top_100_url,
    format_history_url,
    get_fear_greed_index_url,
    search_coin_url,
)
from realtime_crypto.models.types import (
    PerformingCrypto,
    Top100Coin,
    HistoryPoint,
    GreedFearHistoryPoint,
)
import time
from datetime import datetime, timedelta


class RealTimeCrypto:
    def __init__(self):
        self.client = httpx.Client()

    def _fetch_json(self, url: str) -> Optional[dict]:
        try:
            res = self.client.get(url)
            res.raise_for_status()
            return res.json()
        except httpx.HTTPStatusError as e:
            print("Error occured trying to fetch data")
            return None

    def get_coin(self, coin_name: str | int) -> Optional[Coin]:
        """
        Get data of a single coin.
        """

        res = self._fetch_json(get_token_data_url(coin_name))

        if "data" not in res:
            return None

        json_data = res["data"]

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

        price_json = self._fetch_json(get_token_data_url(coin_name))

        if price_json["status"]["error_code"] != "0":
            return 0

        price = price_json["data"]["statistics"]["price"]

        return price

    def get_coin_id(self, coin_name: str) -> int:
        """
        Returns the coinmarketcap id of a given crypto
        """

        res_json = self._fetch_json(get_token_data_url(coin_name))

        if "data" not in res_json:
            return 0

        id = res_json["data"]["id"]
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
        cryptocurrencies = self._fetch_json(get_top_100_url())

        return [
            {
                "name": crypto["name"],
                "symbol": crypto["symbol"],
                "price": crypto["current_price"],
                "rank": crypto["market_cap_rank"],
            }
            for crypto in cryptocurrencies
        ]

    def get_history(self, coin: int | str, range: str) -> list[HistoryPoint] | None:
        """
        Get the price history for a given.
        Example range inputs: 1h, 1d, 7d, 1m, 3m, 1y

        Return example {'id': '1', 'timestamp': '1723334400', 'price': 60944}
        """

        if isinstance(coin, str):
            coin = self.get_coin_id(coin)
            if not coin:
                return None

        history_json = self._fetch_json(format_history_url(coin, range))

        if history_json["status"]["error_code"] != "0":
            return None

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

        res = self._fetch_json(get_fear_greed_index_url(from_unix, to_unix))
        if res is None:
            return []

        res_data = res["data"]
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

        res = self._fetch_json(
            get_fear_greed_index_url(int(yesterday_unix), int(now_unix))
        )
        if res is None:
            return 0

        res_data = res["data"]
        if "dataList" not in res_data:
            return 0

        score = int(res_data["dataList"][0]["score"])

        return score

    def get_best_performing_cryptos(
        self, range: str, reverse=True
    ) -> Optional[list[PerformingCrypto]]:
        """
        Get best performing cryptos in the top 100.

        range examples: 1h, 24h, 7d, 30d, 60d, 90d, 1y

        Return value is sorted high to low
        """

        valid_ranges = ["1h", "24h", "7d", "30d", "60d", "90d", "1y"]
        if range not in valid_ranges:
            return None

        result = []

        top_100_list = self._fetch_json(get_top_100_url())

        if range == "24h":
            sortedli = sorted(
                top_100_list,
                key=lambda d: d["price_change_percentage_24h"],
                reverse=reverse,
            )

            return sortedli

        for coin in top_100_list:
            coin_obj = self.get_coin(coin["id"])

            if coin_obj is None:
                url_data = search_coin_url(coin["name"])
                res = self.client.post(url=url_data["url"], json=url_data["body"])
                searched_coin_slug = res.json()["data"]["suggestions"][1]["tokens"][0][
                    "slug"
                ]
                coin_obj = self.get_coin(searched_coin_slug)
                if coin_obj is None:
                    continue

            price_change = coin_obj.get_statistics().get_price_change(range)
            if price_change:
                result.append(
                    {
                        "symbol": coin_obj.get_symbol(),
                        "slug": coin_obj.get_slug(),
                        "priceChange" + range: price_change,
                    }
                )

        return sorted(result, key=lambda d: d["priceChange" + range], reverse=reverse)

    def search_coin_id(self, search: str) -> Optional[int]:
        """
        Get the coinmarketcap ID if a coin, given a coin name / symbol
        """
        url_data = search_coin_url(search)
        res = self.client.post(url=url_data["url"], json=url_data["body"])
        post_count = res.json()["data"]["suggestions"][0]["postCount"]

        if post_count == "0":
            return None

        searched_coin_id = res.json()["data"]["suggestions"][1]["tokens"][0]["id"]
        return searched_coin_id
