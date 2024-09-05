import os
import logging
import logging.handlers
from datetime import datetime

name = datetime.now().strftime("%Y%m%d_%H%M%S")
logger = logging.getLogger(name)
formatter = logging.Formatter('[%(levelname)s] %(asctime)s > %(message)s')
filename = os.path.join(os.getcwd(), f'{name}.log')
fileMaxByte = 1024 * 1024 * 10  # 10MB
fileHandler = logging.handlers.RotatingFileHandler(
    filename, maxBytes=fileMaxByte, backupCount=10
)
streamHandler = logging.StreamHandler()

fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)
logger.setLevel(logging.DEBUG)


def debug(msg):
    logger.debug(msg)

def info(msg):
    logger.info(msg)

def warning(msg):
    logger.warning(msg)

def error(msg):
    logger.error(msg)

def critical(msg):
    logger.critical(msg)
