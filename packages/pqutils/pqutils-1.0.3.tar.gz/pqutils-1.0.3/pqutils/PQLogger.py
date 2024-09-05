import os
import logging
import logging.handlers
from datetime import datetime

# 클래스 내부에서 사용할 디버그/릴리즈 수준 설정 값
DEF_DEBUG = 0
DEF_RELEASE = 1


class PQLogger:

    def __init__(self, level=DEF_DEBUG):
        """Logger 생성자. level 인자로 DEF_DEBUG 또는 DEF_RELEASE를 받음"""
        self.level = level  # DEF_LEVEL을 인스턴스 변수로 설정

        # 로거 생성
        name = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.logger = logging.getLogger(name)
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s > %(message)s')

        # 로그 파일 설정
        filename = os.path.join(os.getcwd(), f'{name}.log')
        fileMaxByte = 1024 * 1024 * 10  # 10MB
        fileHandler = logging.handlers.RotatingFileHandler(
            filename, maxBytes=fileMaxByte, backupCount=10
        )  # 최대 10개의 파일을 생성, 순환됨
        streamHandler = logging.StreamHandler()

        # 포매터 설정
        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        # 핸들러를 로거에 추가
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(streamHandler)
        self.logger.setLevel(logging.DEBUG)  # 로그 레벨을 디버그로 설정

    # Debug
    def debug(self, msg):
        if self.level == DEF_DEBUG:
            self.logger.debug(msg)

    # Information
    def info(self, msg):
        if self.level == DEF_DEBUG:
            self.logger.info(msg)

    # Warning
    def warning(self, msg):
        if self.level == DEF_DEBUG:
            self.logger.warning(msg)

    # Error
    def error(self, msg):
        self.logger.error(msg)

    # Critical
    def critical(self, msg):
        self.logger.critical(msg)
