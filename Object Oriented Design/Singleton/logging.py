import logging

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._logger = logging.getLogger('app')
            cls._instance._logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler('app.log')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            cls._instance._logger.addHandler(handler)
        return cls._instance

    def log(self, message, level=logging.INFO):
        self._logger.log(level, message)

# Usage
logger = Logger()
logger.log("This is an info message")
logger.log("This is a warning", logging.WARNING)

# Both logs go to the same file because they use the same logger instance