from typing import TypedDict


class Top100Coin(TypedDict):
    name: str
    symbol: str
    price: float


class HistoryPoint(TypedDict):
    id: int
    timestamp: str
    price: float


class GreedFearHistoryPoint(TypedDict):
    score: float
    name: str
    timestamp: str
