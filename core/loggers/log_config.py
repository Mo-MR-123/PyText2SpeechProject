import logging
import os
import sys

from typing import Union
from logging import Logger
from pathlib import Path
from datetime import datetime

LOGGER_IS_DEV = int(os.environ.get("IS_DEV_LOGGING", 1))
ENABLE_LOGGING = int(os.environ.get("ENABLE_LOGGING", 1))

class LoggerStub:
    def __init__(self):
        pass

    def info(self, msg):
        pass
    
    def debug(self, msg):
        pass

    def critical(self, msg):
        pass

    def error(self, msg):
        pass

"""
LogConfig class is responsible for configuring new loggers. 
NOTE: each class making use of logging must create new instance of this class
        and get a new class-specific logger through this class using methods provided.
"""
class LogConfig:
    def __init__(self, log_level=logging.INFO, log_dir='logs'):
        self.log_level = log_level
        self.log_dir = log_dir
        self.name_logger = None
        self.logger = None
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

        self.logger.setLevel(self.log_level)

    def get_logger(self, name) -> Union[Logger, LoggerStub]:
        if not ENABLE_LOGGING:
            return LoggerStub()
            
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)

        self.name_logger = name

        if LOGGER_IS_DEV:
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter(self.log_format, self.date_format))
            self.logger.addHandler(console_handler)
        else:
            # Create logs directory if it doesn't exist
            os.makedirs(self.log_dir, exist_ok=True)

            # File handler
            file_handler = logging.FileHandler(
                Path(self.log_dir).joinpath(
                    Path(f'{name}_{datetime.now().strftime("%Y%m%d")}.log')
                )
            )
            file_handler.setFormatter(logging.Formatter(self.log_format, self.date_format))
            self.logger.addHandler(file_handler)

        return self.logger
