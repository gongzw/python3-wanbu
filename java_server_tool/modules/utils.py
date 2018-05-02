#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/1/18

import json
import os,zipfile

def print_err(msg,quit=False):
    output = "\033[31;1mError: %s\033[0m" % msg
    if quit:
        exit(output)
    else:
        print(output)


def json_parser(json_file):
    '''
    load yaml file and return
    :param yml_filename:
    :return:
    '''

    try:
        f = open(json_file,'r')
        data = json.load(f)
        return data
    except Exception as e:
        print_err(e)


def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    dest_dir = file_name.split('.')[0]
    #print("dest_dir:%s"%dest_dir)
    if os.path.isdir(dest_dir):
        pass
    else:
        os.mkdir(dest_dir)
    for names in zip_file.namelist():
        zip_file.extract(names,dest_dir)
    zip_file.close()



