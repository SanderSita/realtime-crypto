from typing import Optional, TypedDict


class Top100Coin(TypedDict):
    name: str
    symbol: str
    price: float
    rank: int


class HistoryPoint(TypedDict):
    id: int
    timestamp: str
    price: float


class GreedFearHistoryPoint(TypedDict):
    score: float
    name: str
    timestamp: str


class PerformingCrypto(TypedDict):
    id: str
    symbol: str
    name: str
    image: str
    current_price: float
    market_cap: int
    market_cap_rank: int
    fully_diluted_valuation: int
    total_volume: int
    high_24h: float
    low_24h: float
    price_change_24h: float
    price_change_percentage_24h: float
    market_cap_change_24h: int
    market_cap_change_percentage_24h: float
    circulating_supply: float
    total_supply: float
    max_supply: Optional[float]
    ath: float
    ath_change_percentage: float
    ath_date: str
    atl: float
    atl_change_percentage: float
    atl_date: str
    roi: Optional[float]
    last_updated: str
