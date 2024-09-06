from big_thing_py.common import *

from termcolor import colored, cprint

import asyncio
import logging
import os
import time
import re
import io
from enum import Enum
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler, BaseRotatingHandler


class LoggerType(Enum):
    ALL = 0
    FILE = 1
    CONSOLE = 2
    OFF = 3


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class MicrosecondFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = datetime.now().strftime(datefmt)
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
            s = "%s,%03d" % (t, record.msecs)  # 마이크로초까지 출력
        return s


class AsyncRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False, errors=None):
        super().__init__(filename, mode, maxBytes, backupCount, encoding, delay, errors)

        self._loop = asyncio.get_running_loop()

    async def asyncDoRollover(self):
        self.doRollover()

    def doRollover(self):
        self._loop.call_soon_threadsafe(self.asyncDoRollover)


class MXLogger:
    _instance: 'MXLogger' = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MXLogger, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        log_file_name: str = f'mqtt_message.log',
        log_file_path: str = f'./log',
        logger_type: LoggerType = LoggerType.ALL,
        logging_mode: LogLevel = LogLevel.DEBUG,
        async_mode: bool = False,
        max_bytes: int = 100 * 1024 * 1024,  # 100MB
        backup_count: int = 1000000,
    ) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return

        self._log_file_name = log_file_name
        self._log_file_path = log_file_path
        self._logger_type = logger_type
        self._logging_mode = logging_mode
        self._max_bytes = max_bytes
        self._backup_count = backup_count

        self._formatter = MicrosecondFormatter('[%(asctime)s] %(message)s', datefmt='%Y/%m/%d %H:%M:%S.%f')
        self._console_logger = None
        self._file_logger = None

        self._initialized = False
        self._async_mode = async_mode

    def start(self) -> None:
        if self._initialized:
            return

        if self._logger_type == LoggerType.ALL:
            self._set_file_logger()
            self._set_console_logger()
        elif self._logger_type == LoggerType.FILE:
            self._set_file_logger()
        elif self._logger_type == LoggerType.CONSOLE:
            self._set_console_logger()
        else:
            raise ValueError(f'[MXLogger] Not supported logger type...')

        if AsyncRotatingFileHandler in [type(handler) for handler in self._file_logger.handlers]:
            self.MXLOG_WARN(f'Async logging mode on. Timestamp of log couldn\'t be accurate...')

        self._initialized = True

    @classmethod
    def get_instance(cls) -> 'MXLogger':
        return cls._instance

    def _set_file_logger(self) -> None:
        if self._logger_type in [LoggerType.ALL, LoggerType.FILE]:
            os.makedirs('/'.join(self._log_file_path.rstrip('/').split('/')), exist_ok=True)

        self._file_logger = logging.getLogger('file_logger')
        self._file_logger.setLevel(self._logging_mode.value)
        self._file_logger.propagate = False

        try:
            sync_file_handler = RotatingFileHandler(
                filename='/'.join([self._log_file_path, self._log_file_name]),
                maxBytes=self._max_bytes,
                backupCount=self._backup_count,
            )

            if self._async_mode:
                file_handler = AsyncRotatingFileHandler(
                    filename='/'.join([self._log_file_path, self._log_file_name]),
                    maxBytes=self._max_bytes,
                    backupCount=self._backup_count,
                )
            else:
                file_handler = sync_file_handler
        except Exception as e:
            file_handler = sync_file_handler

        file_handler.setFormatter(self._formatter)
        self._file_logger.addHandler(file_handler)

    def _set_console_logger(self) -> None:
        self._console_logger = logging.getLogger('console_logger')
        self._console_logger.setLevel(self._logging_mode.value)
        self._console_logger.propagate = False

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._formatter)
        self._console_logger.addHandler(console_handler)

    def _remove_color(self, msg: str) -> str:
        ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
        msg = ansi_escape.sub('', msg)
        return msg

    def _log_print(self, msg: str, color: str, on_color: str, mode: LogLevel) -> None:
        log_msg = colored(f'[{mode.name}] {msg}', color=color, on_color=on_color)

        if self._logger_type == LoggerType.ALL:
            logger_group = [self._file_logger, self._console_logger]
        elif self._logger_type == LoggerType.FILE:
            logger_group = [self._file_logger]
        elif self._logger_type == LoggerType.CONSOLE:
            logger_group = [self._console_logger]
        elif self._logger_type == LoggerType.OFF:
            logger_group = []
        else:
            raise ValueError(f'[MXLogger] Not supported logging mode...')

        for logger in logger_group:
            if mode == LogLevel.DEBUG:
                logger.debug(log_msg)
            elif mode == LogLevel.INFO:
                logger.info(log_msg)
            elif mode == LogLevel.WARN:
                logger.warning(log_msg)
            elif mode == LogLevel.ERROR:
                logger.error(log_msg)
            elif mode == LogLevel.CRITICAL:
                logger.critical(log_msg)
            else:
                raise ValueError(f'[MXLogger] not supported log level...')

    def MXLOG_DEBUG(self, msg: str, color: str = None) -> None:
        self._log_print(msg, color, on_color=None, mode=LogLevel.DEBUG)

    def MXLOG_INFO(self, msg: str, color: str = 'cyan') -> None:
        self._log_print(msg, color, on_color=None, mode=LogLevel.INFO)

    def MXLOG_WARN(self, msg: str, color: str = 'yellow') -> None:
        self._log_print(msg, color, on_color=None, mode=LogLevel.WARN)

    def MXLOG_ERROR(self, msg: str, color: str = 'red') -> None:
        self._log_print(msg, color, on_color=None, mode=LogLevel.ERROR)

    def MXLOG_CRITICAL(self, msg: str, color: str = None) -> None:
        self._log_print(msg, color, on_color='on_red', mode=LogLevel.CRITICAL)


def MXLOG_DEBUG(msg: List[str], color: str = None) -> None:
    logger = MXLogger.get_instance()
    if not logger:
        raise ValueError(f'[MXLogger] Logger is not initialized...')

    logger.MXLOG_DEBUG(msg, color)


def MXLOG_INFO(msg: List[str], color: str = 'cyan') -> None:
    logger = MXLogger.get_instance()
    if not logger:
        raise ValueError(f'[MXLogger] Logger is not initialized...')

    logger.MXLOG_INFO(msg, color)


def MXLOG_WARN(msg: List[str], color: str = 'yellow') -> None:
    logger = MXLogger.get_instance()
    if not logger:
        raise ValueError(f'[MXLogger] Logger is not initialized...')

    logger.MXLOG_WARN(msg, color)


def MXLOG_ERROR(msg: List[str], color: str = 'red') -> None:
    logger = MXLogger.get_instance()
    if not logger:
        raise ValueError(f'[MXLogger] Logger is not initialized...')

    logger.MXLOG_ERROR(msg, color)


def MXLOG_CRITICAL(msg: List[str], color: str = None) -> None:
    logger = MXLogger.get_instance()
    if not logger:
        raise ValueError(f'[MXLogger] Logger is not initialized...')

    logger.MXLOG_CRITICAL(msg, color)


if __name__ == '__main__':
    sync_mode = False
    function_mode = True

    if function_mode:
        MXLogger(logger_type=LoggerType.ALL, logging_mode=LogLevel.DEBUG).start()

        while True:
            MXLOG_DEBUG('test')
            MXLOG_INFO('test')
            MXLOG_WARN('test')
            MXLOG_ERROR('test')
            MXLOG_CRITICAL('test')

            MXLOG_DEBUG('test', color='red')
            MXLOG_CRITICAL('test', color='yellow')
            time.sleep(1)
    else:
        if sync_mode:
            sync_logger = MXLogger(logger_type=LoggerType.ALL, logging_mode=LogLevel.DEBUG)
            sync_logger.start()

            while True:
                sync_logger.MXLOG_DEBUG('test')
                sync_logger.MXLOG_INFO('test')
                sync_logger.MXLOG_WARN('test')
                sync_logger.MXLOG_ERROR('test')
                sync_logger.MXLOG_CRITICAL('test')

                sync_logger.MXLOG_DEBUG('test', color='red')
                sync_logger.MXLOG_CRITICAL('test', color='yellow')
                time.sleep(1)
        else:

            async def main():
                async_logger = MXLogger(logger_type=LoggerType.ALL, logging_mode=LogLevel.DEBUG)
                async_logger.start()

                while True:
                    async_logger.MXLOG_DEBUG('test')
                    async_logger.MXLOG_INFO('test')
                    async_logger.MXLOG_WARN('test')
                    async_logger.MXLOG_ERROR('test')
                    async_logger.MXLOG_CRITICAL('test')

                    async_logger.MXLOG_DEBUG('test', color='red')
                    async_logger.MXLOG_CRITICAL('test', color='yellow')
                    await asyncio.sleep(1)

            asyncio.run(main())
