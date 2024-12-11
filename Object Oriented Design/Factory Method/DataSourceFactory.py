from abs import ABC abstractmethod

class DataSource(ABC):
    @abstractmethod
    def fetch_data(self, query: str) -> str:
        pass
      
class MarketDataSrouce(DataFactory):
    def fetch_data(self, query: str) -> str:
        return f"Fetching data from market data source for query: {query}"

class HistoricalDataSrouce(DataFactory):
    def fetch_data(self, query: str) -> str:
        return f"Fetching data from historical data source for query: {query}"
      
class InternalDataSrouce(DataFactory):
    def fetch_data(self, query: str) -> str:
        return f"Fetching data from internal data source for query: {query}"    
  
class DataSourceFactory:
  @staticmethod
  def create_data_source(source_type: str) -> DataSource:
    if course_type =='market':
      return MarketDataSrouce()
    elif course_type =='historical':
      return HistoricalDataSrouce()
    elif course_type =='internal':
      return InternalDataSrouce()
    else:
      raise ValueError(f"Invalid data source type: {source_type}")
    
    
market_data = DataSourceFactory.create_data_source('market')
print(market_data.fetch_data('AAPL'))
