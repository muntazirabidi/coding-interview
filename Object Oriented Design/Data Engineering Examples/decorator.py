'''
Use Case: Enhancing data processing functions or adding features to data pipelines, like compression, encryption, or logging.
'''

from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def process(self, data):
        pass

class BaseProcessor(DataProcessor):
    def process(self, data):
        return f"Processing {data}"

class CompressionDecorator(DataProcessor):
    def __init__(self, processor):
        self.processor = processor

    def process(self, data):
        result = self.processor.process(data)
        return f"{result} with Compression"

class EncryptionDecorator(DataProcessor):
    def __init__(self, processor):
        self.processor = processor

    def process(self, data):
        result = self.processor.process(data)
        return f"{result} and Encryption"

# Usage in a quant firm
base = BaseProcessor()
compressed = CompressionDecorator(base)
encrypted = EncryptionDecorator(compressed)

print(encrypted.process("market data"))  # Should print: Processing market data with Compression and Encryption