from typing import Callable
import httpx
from crypto.models.crypto_websocket import CryptoWebsocket
from urls import urls
from crypto.models.coin import Coin
from crypto.models.statistic import Statistic
import asyncio
from crypto.models.websocket_details import WebsocketDetails


class RealtimeCryptoTracker:
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

        return price

    @classmethod
    def get_coin_id(self, coin_name: str) -> int:
        res = self.client.get(urls["token_data"] + coin_name)
        json_data = res.json()["data"]
        id = json_data["id"]
        return int(id)

    async def realtime_prices(self, cryptocurrencies: list[str], callback: Callable):
        crypto_ws = CryptoWebsocket(cryptocurrencies, callback)
        await crypto_ws.websocket_init()

    def get_top_100_coins(self):
        pass


async def main():
    tracker = RealtimeCryptoTracker()
    li = [
        "bitcoin",  # BTC
        "ethereum",  # ETH
        "binancecoin",  # BNB
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
        "monero",  # XMR
        "tezos",  # XTZ
        "vechain",  # VET
        "uniswap",  # UNI
        "shiba-inu",  # SHIB
        "aave",  # AAVE
        "cosmos",  # ATOM
        "filecoin",  # FIL
        "theta",  # THETA
        "algorand",  # ALGO
        "elrond",  # EGLD
        "zcash",  # ZEC
        "decentraland",  # MANA
        "hedera",  # HBAR
        "vechain",  # VET
        "pepe",  # PEPE
        "fantom",  # FTM
        "terra-luna",  # LUNA
        "harmony",  # ONE
        "thorchain",  # RUNE
        "polygon",  # MATIC
        "maker",  # MKR
        "dash",  # DASH
        "neo",  # NEO
        "iota",  # MIOTA
        "eos",  # EOS
        "pancakeswap",  # CAKE
        "zilliqa",  # ZIL
        "enjincoin",  # ENJ
        "chiliz",  # CHZ
        "curve-dao-token",  # CRV
        "compound",  # COMP-
        "yearn-finance",  # YFI
        "basic-attention-token",  # BAT
        "kusama",  # KSM
        "1inch",  # 1INCH
        "sushiswap",  # SUSHI
        "waves",  # WAVES
    ]

    async def print_res(ws_detail: WebsocketDetails):
        print(ws_detail.get_crypto(), ws_detail.get_new_price())

    asyncio.create_task(tracker.realtime_prices(li, print_res))

    print("HEREEEE")
    await asyncio.sleep(200000)


if __name__ == "__main__":
    asyncio.run(main())
