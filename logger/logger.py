import logging
from logging.handlers import RotatingFileHandler


class AppLogger:
    def __init__(self, name: str, log_file: str = "app.log", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            file_handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=3)
            file_handler.setLevel(level)

            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger


logger = AppLogger("app_logger").get_logger()
