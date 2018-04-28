#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/4/11

import os,sys
BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BaseDir)
sys.path.append(BaseDir)



import logging
import logging.config
from modules import utils


def log_hander():
    '''
    日志管理
    :return:
    '''
    # config_path = os.path.join("conf/", 'logging.conf')
    # logging.config.fileConfig(config_path)
    # return logging.getLogger()

    log_conf = utils.get_config('log')
    logger_name = log_conf["log_name"]
    logger_level = log_conf["log_level"]
    logger = logging.getLogger(logger_name)
    if not logger.handlers:
        level = eval(logger_level)
        logger.setLevel(level)
        logger_dir = log_conf["log_path"]
        if not os.path.exists(logger_dir):
            os.mkdir(logger_dir)
        logger_file = os.path.join(logger_dir, logger_name)
        fh = logging.FileHandler(logger_file)
        fh.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

# if __name__ == "__main__":
#     log_hander().debug("向用户 {0} 号码 {1} 发送短信 {2} 成功.")
