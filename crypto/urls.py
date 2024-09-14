# API URLS


def get_token_data_url(slug: str | int) -> str:
    return f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/?{'slug' if isinstance(slug, str) else 'id'}={slug}"


def format_history_url(coin_id: int | str, range: str = "1D") -> str:
    return f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={coin_id}&range={range}"


def get_top_100_url() -> str:
    return "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100"


def get_fear_greed_index_url(start: int, end: int) -> str:
    return f"https://api.coinmarketcap.com/data-api/v3/fear-greed/chart?start={start}&end={end}"


def search_coin_url(keyword):
    return {
        "url": "https://api.coinmarketcap.com/gravity/v4/gravity/global-search",
        "body": {"keyword": keyword, "limit": 1, "scene": "community"},
    }
