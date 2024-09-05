# @Project: diff-kit
# @Time: 2024/9/2 10:24
# @Author: Alan
# @File: logger

import os
import sys
from pathlib import Path
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent

LOGURU_FILE = {
    "is_show": "on",
    "level": "INFO",
    'path': os.path.join(BASE_DIR, 'logs', 'run{time:YYYY-MM-DD}.log'),
    "rotation": "10MB",
    'retention': "7 days",
}
LOGURU_CONSOLE = {
    "is_show": "on",
    "level": "INFO",
}


class LoguruConfigurator:
    def __init__(self):
        self._file_set = LOGURU_FILE
        self._console_set = LOGURU_CONSOLE

    def configure(self):
        # 清除所有现有的日志处理器（如果有的话）
        logger.remove()
        # 控制台输出
        if self._console_set.get('is_show', '').lower() == "on":
            level = self._console_set.get('level', 'INFO')
            logger.add(
                sink=sys.stderr,
                format="[<green>{time:YYYY-MM-DD HH:mm:ss}</green> {level:<8}| "
                       "<cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                       "<level>{message}</level>",
                level=level,
            )
            # 文件保存
        if self._file_set.get('is_show', '').lower() == "on":
            log_path = self._file_set.get('path', os.path.join(Path(__file__).parent.parent.parent, 'logs',
                                                               'test{time:YYYY-MM-DD}.log'))
            level = self._file_set.get('level', 'INFO')
            rotation = self._file_set.get('rotation', '10MB')
            retention = self._file_set.get('retention', '7 days')
            logger.add(
                log_path,
                rotation=rotation,
                retention=retention,
                compression='zip',
                encoding="utf-8",
                enqueue=True,
                format="[{time:YYYY-MM-DD HH:mm:ss} {level:<6} | {file}:{module}.{function}:{line}]  {message}",
                level=level,
            )


configurator = LoguruConfigurator()
configurator.configure()