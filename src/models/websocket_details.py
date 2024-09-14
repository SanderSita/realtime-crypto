class WebsocketDetails:
    def __init__(
        self,
        id: int,
        crypto: str,
        price: float,
        p24: float,
        p7d: float,
        p30d: float,
        p3m: float,
        p1y: float,
        pytd: float,
        p_all: float,
        mc: float,
    ):
        self.id = id
        self.crypto = crypto
        self.price = price  # current price
        self.p24 = p24  # 24-hour price change
        self.p7d = p7d  # 7-day price change
        self.p30d = p30d  # 30-day price change
        self.p3m = p3m  # 3-month price change
        self.p1y = p1y  # 1-year price change
        self.pytd = pytd  # Year-to-date price change
        self.p_all = p_all  # All-time price change
        self.mc = mc  # Market capitalization

    def get_id(self) -> int:
        return self.id

    def get_new_price(self) -> float:
        return self.price

    def get_crypto(self) -> str:
        return self.crypto

    def get_p24(self) -> float:
        return self.p24

    def get_p7d(self) -> float:
        return self.p7d

    def get_p30d(self) -> float:
        return self.p30d

    def get_p3m(self) -> float:
        return self.p3m

    def get_p1y(self) -> float:
        return self.p1y

    def get_pytd(self) -> float:
        return self.pytd

    def get_p_all(self) -> float:
        return self.p_all

    def get_mc(self) -> float:
        return self.mc
