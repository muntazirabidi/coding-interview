class MarketData:
    def __init__(self):
        self._observers = []
        self.data = None

    def attach(self, observer):
        self._observers.append(observer)

    def update_data(self, new_data):
        self.data = new_data
        self.notify()

    def notify(self):
        for observer in self._observers:
            observer.update(self.data)

class Trader:
    def update(self, data):
        print(f"Trader updated with new market data: {data}")

class RiskManager:
    def update(self, data):
        print(f"RiskManager updated with new market data: {data}")

# Usage in a quant firm
market_data = MarketData()
trader = Trader()
risk_manager = RiskManager()

market_data.attach(trader)
market_data.attach(risk_manager)

market_data.update_data("New stock price: $150")  # Both trader and risk_manager get notified