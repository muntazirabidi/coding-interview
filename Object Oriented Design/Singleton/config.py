class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {}  # Initialize the config dictionary
        return cls._instance

    def load_config(self, config_data):
        self._config.update(config_data)

    def get(self, key):
        return self._config.get(key, None)

# Usage
config = Config()
config.load_config({'debug': True, 'api_key': '12345'})

print(config.get('debug'))  # True
print(config.get('api_key'))  # 12345