'''
Use Case: Iterating over large datasets or time series data without exposing the underlying data structure.
'''

class MarketDataIterator:
    def __init__(self, data):
        self._data = data
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._data):
            result = self._data[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

# Usage in a quant firm
market_data = ["Price at 9:00", "Price at 10:00", "Price at 11:00"]
data_iterator = MarketDataIterator(market_data)

for item in data_iterator:
    print(item)