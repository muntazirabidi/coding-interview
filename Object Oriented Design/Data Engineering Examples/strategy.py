from abc import ABC, abstractmethod

class TradingStrategy(ABC):
    @abstractmethod
    def execute(self, market_data):
        pass

class MomentumStrategy(TradingStrategy):
    def execute(self, market_data):
        return f"Buy based on momentum: {market_data}"

class MeanReversionStrategy(TradingStrategy):
    def execute(self, market_data):
        return f"Sell based on mean reversion: {market_data}"

class TradingSystem:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_trade(self, market_data):
        return self.strategy.execute(market_data)

# Usage in a quant firm
market_data = "Current price is $100"
system = TradingSystem(MomentumStrategy())
print(system.execute_trade(market_data))  # Buy based on momentum

system.set_strategy(MeanReversionStrategy())
print(system.execute_trade(market_data))  # Sell based on mean reversion