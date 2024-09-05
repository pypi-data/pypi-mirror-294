import os
import logging
import logging.handlers
from datetime import datetime

DEF_DEBUG = 0
DEF_RELEASE = 1
DEF_LEVEL = DEF_DEBUG

class PQLogger:
    global logger

    def __init__(self):
        name = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger = logging.getLogger(name)
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s > %(message)s')
        filename = os.getcwd() + '/' + name + '.log'
        fileMaxByte = 1024 * 1024 * 10  # 10MB
        fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte,
                                                           backupCount=10)  # 10개 파일, overwrite 됨
        streamHandler = logging.StreamHandler()
        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        logger.addHandler(streamHandler)
        logger.setLevel(logging.DEBUG)


    # Debug
    def debug(msg):
        if DEF_LEVEL == DEF_DEBUG:
            logger.debug(msg)


    # Information
    def info(msg):
        if DEF_LEVEL == DEF_DEBUG:
            logger.info(msg)


    # Warming
    def warning(msg):
        if DEF_LEVEL == DEF_DEBUG:
            logger.warning(msg)


    # Error
    def error(msg):
        logger.error(msg)


    # Critical
    def critical(msg):
        logger.critical(msg)
