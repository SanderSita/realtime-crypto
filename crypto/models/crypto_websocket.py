from typing import Callable
import websockets
import json
import requests


class CryptoWebsocket:
    def __init__(
        self,
        crypto_names: list[str],
        callback: Callable,
    ):
        self.uri = "wss://push.coinmarketcap.com/ws"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"
        }
        self.crypto_names = crypto_names
        self.callback = callback

    async def websocket_init(self):
        print(self.crypto_names)

        crypto_ids = list()
        for name in self.crypto_names:
            res = requests.get(
                "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/?slug="
                + name
            )
            json_data = res.json()["data"]
            id = str(json_data["id"])
            print(id)
            crypto_ids.append(id)
        print(",".join(crypto_ids))
        async with websockets.connect(self.uri, extra_headers=self.headers) as ws:
            # {"method":"RSUBSCRIPTION","params":["main-site@crypto_price_5s@{}@normal","1,1027,825,1839,5426,3408,52,74,1958,11419,2010,5805,5994,1975,183"]}
            msg = {
                "method": "RSUBSCRIPTION",
                "params": [
                    "main-site@crypto_price_5s@{}@normal",
                    "1",
                ],
            }
            await ws.send(json.dumps(msg))

            # Listen for messages
            async for message in ws:
                await self.callback(message)
