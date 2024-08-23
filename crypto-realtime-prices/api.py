import httpx
from urls import urls

class API:
    def __init__(self):
        pass
    
    def get_coin_data(self, slug: str):
        res = httpx.get(urls["token_data"] + slug)
        json_data = res.json()
        return json_data
    
    def get_current_price(self, slug: str):
        pass
    
    def get_realtime_price(self, slug: str):
        pass
    
if __name__ == "__main__":
    api = API()
    coin_data = api.get_coin_data("bitcoin")
    print(coin_data)