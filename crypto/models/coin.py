from typing import Optional
import httpx
from crypto.models.crypto_websocket import CryptoWebsocket
from crypto.models.types import HistoryPoint
from crypto.urls import format_history_url, get_token_data_url
from crypto.models.statistic import Statistic


class Coin:
    def __init__(
        self, id: int, symbol: str, slug: str | int, desc: str, price_stats: Statistic
    ) -> None:
        self.id = id
        self.symbol = symbol
        self.slug = slug
        self.description = desc
        self.price_stats = price_stats
        self.price = price_stats.get_price()

    def get_id(self) -> int:
        return self.id

    def get_slug(self) -> str | int:
        return self.slug

    def get_symbol(self) -> str:
        return self.symbol

    def get_description(self) -> str:
        return self.description

    def get_statistics(self) -> Statistic:
        """
        Get statistics for this coin.
        """
        return self.price_stats

    @classmethod
    def get_current_price(self, slug: str):
        """
        Fetch the current price of a cryptocurrency by its slug.
        Example usage: Coin.get_current_price('bitcoin')
        """

        res = httpx.get(get_token_data_url(slug))
        if res.status_code != 200:
            raise Exception(f"Failed to fetch data for {slug}: {res.text}")

        json_data = res.json()
        if json_data["status"]["error_code"] != "0":
            raise Exception(
                f"Error in response: {json_data['status']['error_message']}"
            )

        new_price = json_data["data"]["statistics"]["price"]
        self.price = new_price
        return new_price

    def get_price(self):
        return self.price

    async def get_realtime_price(self, callback):
        crypto_ws = CryptoWebsocket([self.get_slug()], callback)
        await crypto_ws.websocket_init()

    def get_history(self, range: str) -> Optional[list[HistoryPoint]]:
        """
        Get the price history.
        Example range inputs: 1h, 1d, 7d, 1m, 3m, 1y

        Return example [{'id': '1', 'timestamp': '1723334400', 'price': 60944}]
        """

        history = httpx.get(format_history_url(self.id, range))
        history_json = history.json()

        if history_json["status"]["error_code"] != "0":
            return None

        history_data = history_json["data"]["points"]

        return [
            {"id": self.id, "timestamp": point, "price": history_data[point]["v"][0]}
            for point in history_data
        ]

    def __repr__(self) -> str:
        return f"this is {self.symbol}"
