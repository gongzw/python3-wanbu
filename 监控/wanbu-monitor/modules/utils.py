#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/4/10

import os
from configparser import ConfigParser

BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__) ))
#print(BaseDir)

def get_config(sections):
    config = ConfigParser()
    config_path = '{0}/conf/config.ini'.format(BaseDir)
    config.read(config_path)
    conf_items = dict(config.items(sections))
    print(conf_items)
    return conf_items




if __name__ == "__main__":
    get_config('cmdb_config')
