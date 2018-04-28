#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/4/10


from modules import mydb
from modules import utils

def db_handler_ExecQuery(dic):
    ## ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
    ## #返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
    ## ms.ExecNonQuery("insert into WeiBoUser values('2','3')")


    mysql_obj = mydb.MSSQL(dic)
    return mysql_obj.ExecQuery


def db_handler_ExecNonQuery(dic):
    mysql_obj = mydb.MSSQL(dic)
    return mysql_obj.ExecNonQuery