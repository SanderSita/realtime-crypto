class Coin:
    def __init__(self, symbol: str, desc: str) -> None:
        self.symbol = symbol
        self.description = desc
        
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_description(self) -> str:
        return self.description
    
    def __repr__(self) -> str:
        return f"this is {self.symbol}"