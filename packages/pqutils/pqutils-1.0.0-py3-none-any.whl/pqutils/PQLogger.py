import os
import logging
import logging.handlers
from datetime import datetime


DEF_DEBUG = 0
DEF_RELEASE = 1
DEF_LEVEL = DEF_DEBUG


def Logger():
    # 로거 인스턴스를 만든다
    global logger
    name = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger = logging.getLogger(name)

    # 포매터를 만든다
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s > %(message)s')

    # 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
    filename = os.getcwd() + '/' + name + '.log'
    fileMaxByte = 1024 * 1024 * 10  # 10MB
    fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte,
                                                       backupCount=10)  # 10개 파일, overwrite 됨
    streamHandler = logging.StreamHandler()

    # 각 핸들러에 포매터를 지정한다.
    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)

    # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)


# Debug
def logger_debug(msg):
    if DEF_LEVEL == DEF_DEBUG:
        logger.debug(msg)


# Information
def logger_info(msg):
    if DEF_LEVEL == DEF_DEBUG:
        logger.info(msg)


# Warming
def logger_warning(msg):
    if DEF_LEVEL == DEF_DEBUG:
        logger.warning(msg)


# Error
def logger_error(msg):
    logger.error(msg)


# Critical
def logger_critical(msg):
    logger.critical(msg)
