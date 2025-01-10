# -*- coding: utf-8 -*-

import logging
import os

from config.basic_setting import LOG_PATH, SERVICE_MODE
from logging.handlers import TimedRotatingFileHandler
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("httpcore.connection").setLevel(logging.WARNING)

class InitLog(object):
    def __init__(self):
        self.log_path = LOG_PATH
        self.formatter = logging.Formatter(
            '[%(asctime)s] -- [%(name)s] -- [%(levelname)s] -- [%(filename)s:%(lineno)d] -- %(message)s'
        )
        self.log_level = {
            'product': logging.DEBUG,
            'develop': logging.DEBUG,
            'testing': logging.DEBUG,
        }

    def setup_log(self):
        """配置日志"""
        # 设置日志的记录等级
        access_file_log_handler = self.generate_handler(when='midnight', filename='access', level=logging.DEBUG)
        error_file_log_handler = self.generate_handler(when='midnight', filename='error', level=logging.ERROR)
        handlers = [access_file_log_handler, error_file_log_handler]
        global_logger = self.add_handler(None, handlers)
        return global_logger

    def generate_handler(self, when, filename, level):
        handler = TimedRotatingFileHandler(
            os.path.join(self.log_path, f'{filename}-{SERVICE_MODE}.log'),
            backupCount=7,
            when=when,
            interval=1,
            encoding='utf-8',
        )
        handler.setFormatter(self.formatter)
        handler.setLevel(level)
        return handler

    def add_handler(self, logger_name, handlers):
        custom_logger = logging.getLogger(logger_name) if logger_name else logging.getLogger()
        if custom_logger.hasHandlers():
            custom_logger.handlers.clear()
        custom_logger.setLevel(self.log_level.get(SERVICE_MODE))
        for handler in handlers:
            custom_logger.addHandler(handler)
        console_handler = logging.StreamHandler()
        console_handler.name = "console"
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(self.formatter)
        custom_logger.addHandler(console_handler)
        return custom_logger

    def create_log(self):
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        return self.setup_log()
