from typing import Any, Type
import httpx
from crypto.models.crypto_websocket import CryptoWebsocket
from crypto.urls import urls
from crypto.models.statistic import Statistic
import json
import websockets


class Coin:
    def __init__(
        self, id: int, symbol: str, slug: str, desc: str, price_stats: Statistic
    ) -> None:
        self.id = id
        self.symbol = symbol
        self.slug = slug
        self.description = desc
        self.price_stats = price_stats
        self.price = price_stats.get_price()

    def get_id(self) -> int:
        return self.id

    def get_symbol(self) -> str:
        return self.symbol

    def get_description(self) -> str:
        return self.description

    def get_statistics(self) -> Statistic:
        return self.price_stats

    def get_current_price(self):
        res = httpx.get(urls["token_data"] + self.slug)
        new_price = res.json()["data"]["statistics"]["price"]
        self.price = new_price
        return self.price

    @classmethod
    def get_price(cls, slug: str):
        """
        Fetch the current price of a cryptocurrency by its slug.
        Example usage: Coin.get_price('bitcoin')
        """
        res = httpx.get(urls["token_data"] + slug)
        if res.status_code != 200:
            raise Exception(f"Failed to fetch data for {slug}: {res.text}")

        json_data = res.json()
        if json_data["status"]["error_code"] != "0":
            raise Exception(
                f"Error in response: {json_data['status']['error_message']}"
            )

        new_price = json_data["data"]["statistics"]["price"]
        return new_price

    def get_realtime_price(self, callback):
        crypto_socket = CryptoWebsocket(callback)

    def __repr__(self) -> str:
        return f"this is {self.symbol}"
