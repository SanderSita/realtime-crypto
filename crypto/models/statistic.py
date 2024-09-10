from typing import Optional


class Statistic:
    def __init__(self, **kwargs) -> None:
        self.price = kwargs.get("price")
        self.priceChangePercentage1h = kwargs.get("priceChangePercentage1h")
        self.priceChangePercentage24h = kwargs.get("priceChangePercentage24h")
        self.priceChangePercentage7d = kwargs.get("priceChangePercentage7d")
        self.priceChangePercentage30d = kwargs.get("priceChangePercentage30d")
        self.priceChangePercentage60d = kwargs.get("priceChangePercentage60d")
        self.priceChangePercentage90d = kwargs.get("priceChangePercentage90d")
        self.priceChangePercentage1y = kwargs.get("priceChangePercentage1y")
        self.priceChangePercentageAll = kwargs.get("priceChangePercentageAll")
        self.marketCap = kwargs.get("marketCap")
        self.marketCapChangePercentage24h = kwargs.get("marketCapChangePercentage24h")
        self.fullyDilutedMarketCap = kwargs.get("fullyDilutedMarketCap")
        self.fullyDilutedMarketCapChangePercentage24h = kwargs.get(
            "fullyDilutedMarketCapChangePercentage24h"
        )
        self.circulatingSupply = kwargs.get("circulatingSupply")
        self.totalSupply = kwargs.get("totalSupply")
        self.maxSupply = kwargs.get("maxSupply")
        self.marketCapDominance = kwargs.get("marketCapDominance")
        self.rank = kwargs.get("rank")
        self.roi = kwargs.get("roi")
        self.low24h = kwargs.get("low24h")
        self.high24h = kwargs.get("high24h")
        self.low7d = kwargs.get("low7d")
        self.high7d = kwargs.get("high7d")
        self.low30d = kwargs.get("low30d")
        self.high30d = kwargs.get("high30d")
        self.low90d = kwargs.get("low90d")
        self.high90d = kwargs.get("high90d")
        self.low52w = kwargs.get("low52w")
        self.high52w = kwargs.get("high52w")
        self.lowAllTime = kwargs.get("lowAllTime")
        self.highAllTime = kwargs.get("highAllTime")
        self.lowAllTimeChangePercentage = kwargs.get("lowAllTimeChangePercentage")
        self.highAllTimeChangePercentage = kwargs.get("highAllTimeChangePercentage")
        self.lowAllTimeTimestamp = kwargs.get("lowAllTimeTimestamp")
        self.highAllTimeTimestamp = kwargs.get("highAllTimeTimestamp")
        self.lowYesterday = kwargs.get("lowYesterday")
        self.highYesterday = kwargs.get("highYesterday")
        self.openYesterday = kwargs.get("openYesterday")
        self.closeYesterday = kwargs.get("closeYesterday")
        self.priceChangePercentageYesterday = kwargs.get(
            "priceChangePercentageYesterday"
        )
        self.volumeYesterday = kwargs.get("volumeYesterday")
        self.turnover = kwargs.get("turnover")
        self.ytdPriceChangePercentage = kwargs.get("ytdPriceChangePercentage")
        self.volumeRank = kwargs.get("volumeRank")
        self.volumeMcRank = kwargs.get("volumeMcRank")
        self.mcTotalNum = kwargs.get("mcTotalNum")
        self.volumeTotalNum = kwargs.get("volumeTotalNum")
        self.volumeMcTotalNum = kwargs.get("volumeMcTotalNum")

    def get_price(self) -> Optional[float]:
        return self.price

    def get_price_change(self, range: str) -> Optional[float]:
        attribute_name = "priceChangePercentage" + range
        price_change = getattr(self, attribute_name, None)

        return float(price_change) if price_change else None
