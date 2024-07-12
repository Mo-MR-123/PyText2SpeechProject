import logging
import os
from datetime import datetime

class LogConfig:
    def __init__(self, log_level=logging.INFO, log_dir='logs', is_dev=True):
        self.log_level = log_level
        self.log_dir = log_dir
        self.is_dev = is_dev
        self.name_logger = None
        self.log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.date_format = '%Y-%m-%d %H:%M:%S'

    def set_log_level(log_level: int) -> None:
        assert log_level in [logging.INFO, logging.DEBUG, logging.CRITICAL, logging.ERROR, logging.FATAL], f"Invalid log level {log_level}"

        if log_level == logging.INFO:
            self.log_level = logging.INFO 
        elif log_level == logging.DEBUG:
            self.log_level = logging.DEBUG
        elif log_level == logging.CRITICAL:
            self.log_level = logging.CRITICAL
        elif log_level == logging.ERROR:
            self.log_level = logging.ERROR
        elif log_level == logging.FATAL:
            self.log_level = logging.FATAL
        else:
            raise ValueError(f"{self.name_logger} -> Incorrect logging level given = {log_level}")

    def get_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)

        self.name_logger = name

        if self.is_dev:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(self.log_format, self.date_format))
            logger.addHandler(console_handler)
        else:
            # Create logs directory if it doesn't exist
            os.makedirs(self.log_dir, exist_ok=True)

            # File handler
            file_handler = logging.FileHandler(
                os.path.join(self.log_dir, f'{name}_{datetime.now().strftime("%Y%m%d")}.log')
            )
            file_handler.setFormatter(logging.Formatter(self.log_format, self.date_format))
            logger.addHandler(file_handler)

        return logger
