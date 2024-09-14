from typing import Callable
import websockets
import json
import requests
from crypto.models.websocket_details import WebsocketDetails
from crypto.urls import get_token_data_url


class CryptoWebsocket:
    def __init__(
        self,
        cryptocurrencies: list[str],
        callback: Callable,
    ):
        self.uri = "wss://push.coinmarketcap.com/ws"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"
        }
        self.cryptocurrencies = cryptocurrencies
        self.callback = callback

    async def websocket_init(self):
        crypto_ids = {}
        for name in self.cryptocurrencies:
            res = requests.get(get_token_data_url(name))
            json_res = res.json()
            if "data" in json_res:
                id = str(json_res["data"]["id"])
                crypto_ids[id] = name
            else:
                print(
                    f"{name} not found, please make sure the name is correct in the coinmarketcap url"
                )
        websockets
        async with websockets.connect(self.uri, extra_headers=self.headers) as ws:
            msg = {
                "method": "RSUBSCRIPTION",
                "params": [
                    "main-site@crypto_price_5s@{}@normal",
                    ",".join(list(crypto_ids.keys())),
                ],
            }
            await ws.send(json.dumps(msg))

            # Listen for messages
            async for message in ws:
                msg = json.loads(message)
                if "d" in msg:
                    msg_data = msg["d"]
                    ws_detail = WebsocketDetails(
                        id=msg_data["id"],
                        crypto=crypto_ids[str(msg_data["id"])],
                        price=msg_data["p"],
                        p24=msg_data["p24h"],
                        p7d=msg_data["p7d"],
                        p30d=msg_data["p30d"],
                        p3m=msg_data["p3m"],
                        p1y=msg_data["p1y"],
                        pytd=msg_data["pytd"],
                        p_all=msg_data["pall"],
                        mc=msg_data["mc"],
                    )
                    await self.callback(ws_detail)
