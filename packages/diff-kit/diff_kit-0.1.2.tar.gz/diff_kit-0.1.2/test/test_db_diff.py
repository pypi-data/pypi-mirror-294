import os
import sys
from datetime import datetime
from pathlib import Path

import yaml

from diff_kit.utils.logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
from diff_kit.db_diff.core import DbDiffRunner


def read_yaml(file_name):
    """
    读取配置文件
    """
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"File not found: {file_name}")

    if not file_name.endswith(('yaml', 'yml')):
        raise ValueError("File must be a yaml file")

    with open(file_name, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    return data


def main():
    """
    主函数，遍历配置文件并执行对比。
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    config_directory = os.path.join(current_dir, 'config')
    for file in os.listdir(config_directory):
        file_path = os.path.join(config_directory, file)
        config = read_yaml(file_path)
        config['report_name'] = f"{config['db_name_a']}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        if config.get('is_diff', False) is True:
            logger.info(f"run config file: {file_path}")
            DbDiffRunner(**config).diff()


if __name__ == '__main__':
    main()
