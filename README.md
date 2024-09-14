RealTimeCrypto
======

Get crypto prices and coin data from CoinmarketCap, using a simple API.

Installation
------------

The easiest way to install the latest version from PyPI is by using
[pip](https://pip.pypa.io/):

    pip install realtime-crypto

Alternatively, install directly from the GitHub repository:

    pip install git+https://github.com/SanderSita/realtime-crypto-prices.git


Usage
------------
```python
from realtime-crypto import RealTimeCrypto
import asyncio

tracker = RealTimeCrypto()

# Get bitcoin price
bitcoin = tracker.get_coin("bitcoin")
price = bitcoin.get_price()
print(price)

# Get price history
bitcoin.get_history("1Y")

# Get ethereum stats
eth = tracker.get_coin("ethereum")
high24h = eth.get_statistics().high24h
eth_1h = eth.get_statistics().get_price_change("1h")
eth_24h = eth.get_statistics().get_price_change("24h")
eth_1y = eth.get_statistics().get_price_change("1y")

# Get fear and greed index
tracker.get_current_fear_greed_index()

# Get best performing cryptos
tracker.get_best_performing_cryptos("24h")

# Get realtime crypto prices
async def main():
    async def callback(data):
        new_price = data.get_new_price()
        name = ws_detail.get_crypto()
        print(f"{name}: {new_price}")

    # Track bitcoin price
    bitcoin = tracker.get_coin("bitcoin")
    asyncio.create_task(bitcoin.get_realtime_price(callback))

    # Track multiple coins
    coins = ["ethereum", "dogecoin", "pepe"]
    asyncio.create_task(tracker.realtime_prices(coins, callback))

    # Ensure script doesn't close
    await asyncio.sleep(1000)

asyncio.run(main())
```

