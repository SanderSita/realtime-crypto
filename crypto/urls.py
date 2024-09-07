# API URL EXAMPLES
# https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/?slug=vechain


def get_token_data_url(slug: str) -> str:
    return (
        f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/?slug={slug}"
    )


def format_history_url(coin_id: int | str, range: str = "1D") -> str:
    return f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={coin_id}&range={range}"


def get_top_100_url() -> str:
    return "https://api.coincap.io/v2/assets"


def get_fear_greed_index_url(start: int, end: int) -> str:
    return f"https://api.coinmarketcap.com/data-api/v3/fear-greed/chart?start={start}&end={end}"
