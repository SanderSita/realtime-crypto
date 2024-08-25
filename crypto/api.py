import httpx
from urls import urls
from crypto.models.coin import Coin
from crypto.models.statistic import Statistic

class API:
    def __init__(self):
        self.client = httpx.Client()
    
    def get_coin(self, slug: str) -> Coin:
        res = self.client.get(urls["token_data"] + slug)
        json_data = res.json()['data']
        
        price_stats = Statistic(**json_data['statistics'])
        
        id = json_data['id']
        print(id)
        desc = json_data['description']
        symbol = json_data['symbol']
        coin_obj = Coin(id, symbol, slug, desc, price_stats)
        return coin_obj
    
    """
    slug: provide the slug of a coin, for example https://coinmarketcap.com/currencies/bitcoin/ -> "bitcoin"
    """
    def get_current_price(self, slug: str):
        res = self.client.get(urls['token_data'] + slug)
        price_json = res.json()
        
        if price_json['status']['error_code'] != "0":
            return 0
        
        price = price_json['data']['statistics']['price']
        return price
    
    def get_top_100_coins(self):
        pass
    
if __name__ == "__main__":
    api = API()
    # coin_data = api.get_coin_data("bitcoin")
    # print(coin_data)
    # price = api.get_current_price('vechain')
    # print(price)
    coin = api.get_coin("bitcoin")
    coin.websocket_init()
    