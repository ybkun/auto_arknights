#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/12/11 22:06 
# @Author : ybkun 
# @File : log_utils.py 
# @Software: PyCharm

import sys
import logging
from logging.handlers import TimedRotatingFileHandler


def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)
    file_handler = TimedRotatingFileHandler(name + ".log", when='d', interval=1, backupCount=7, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(level)
    return logger
