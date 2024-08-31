# API URL EXAMPLES
# https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/?slug=vechain

urls = {
    "token_data": "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/?slug=",
}


def get_token_data_url(slug: str) -> str:
    return (
        f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/?slug={slug}"
    )


def format_detail_url(coin_id: int | str, range: str = "1D") -> str:
    return f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={coin_id}&range={range}"
