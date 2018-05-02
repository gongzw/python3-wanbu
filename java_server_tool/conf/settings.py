#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/1/18


import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = {
    'engine': 'file_storage',#以文件方式存储
    'name': 'server_info.json',
    'path': "%s/conf" %BASE_DIR,
    'update_file_dir':'%s/files'%BASE_DIR,
    'config_file_dir':'%s/templates'%BASE_DIR,
    'roll_back_dir':'%s/history_versions'%BASE_DIR,
    'tomcat_script_name':'gongcheng.sh'
}




