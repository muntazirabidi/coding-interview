'''
Use Case: Integrating different data sources or legacy systems into a unified data pipeline, adapting interfaces.
'''

class OldMarketDataSource:
    def get_data(self):
        return "Legacy market data"

class NewMarketDataSource:
    def fetch_data(self):
        return "New market data"

class MarketDataSourceAdapter:
    def __init__(self, source):
        self.source = source

    def get_data(self):
        if hasattr(self.source, 'fetch_data'):
            return self.source.fetch_data()
        elif hasattr(self.source, 'get_data'):
            return self.source.get_data()
        else:
            raise ValueError("Unsupported data source")

# Usage in a quant firm
old_source = OldMarketDataSource()
new_source = NewMarketDataSource()

adapter_old = MarketDataSourceAdapter(old_source)
adapter_new = MarketDataSourceAdapter(new_source)

print(adapter_old.get_data())  # Should print: Legacy market data
print(adapter_new.get_data())  # Should print: New market data