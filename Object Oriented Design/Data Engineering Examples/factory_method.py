from abc import ABC, abstractmethod

class DataLoader(ABC):
    @abstractmethod
    def load_data(self):
        pass

class CSVLoader(DataLoader):
    def load_data(self):
        return "Loading data from CSV"

class SQLLoader(DataLoader):
    def load_data(self):
        return "Loading data from SQL"

class DataLoaderFactory:
    def get_loader(self, type):
        if type == "csv":
            return CSVLoader()
        elif type == "sql":
            return SQLLoader()
        else:
            raise ValueError("Unknown data loader type")

# Usage in a quant firm
factory = DataLoaderFactory()
csv_loader = factory.get_loader("csv")
print(csv_loader.load_data())  # Should print: Loading data from CSV
sql_loader = factory.get_loader("sql")
print(sql_loader.load_data())  # Should print: Loading data from SQL