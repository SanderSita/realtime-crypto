from typing import Any, Type
import httpx
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

    def get_price(self):
        res = httpx.get(urls["token_data"] + self.slug)
        new_price = res.json()["data"]["statistics"]["price"]
        self.price = new_price
        return self.price

    def get_realtime_price(self):
        pass

    def __repr__(self) -> str:
        return f"this is {self.symbol}"

    def on_message(self, ws, message):
        json_dict = json.loads(message)
        id = json_dict["d"]["id"]
        new_price = json_dict["d"]["p"]
        self.price = new_price
        print(self.symbol, self.price)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws):
        print("Opened connection")

    async def websocket_init(self, callback):
        uri = "wss://push.coinmarketcap.com/ws"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"
        }

        async with websockets.connect(uri, extra_headers=headers) as ws:
            msg = {
                "method": "RSUBSCRIPTION",
                "params": ["main-site@crypto_price_5s@{}@normal", f"{self.id}"],
            }
            await ws.send(json.dumps(msg))

            # Listen for messages
            async for message in ws:
                callback(message)
