#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/4/10


import pymysql


class MSSQL(object):
    """
    对pymssql的简单封装
    pymssql库，该库到这里下载：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
    使用该库时，需要在Sql Server Configuration Manager里面将TCP/IP协议开启

    用法：

    """

    def __init__(self,dic):
        self.__config__ = dic
        self.host = dic['host']

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        self.conn = pymysql.connect(**self.__config__)
        cur = self.conn.cursor()
        if not cur:
            print("\033[31;1m 数据库连接失败...、\033[0m")
            raise(NameError,"连接数据库失败")

        else:
            print("\033[34;1m 数据库:%s已连接...、\033[0m"%self.host)
            return cur

    def ExecQuery(self,sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        调用示例：
                ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
                for (id,NickName) in resList:
                    print str(id),NickName
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        """
        执行非查询语句

        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        print("exec sql:%s"%sql)
        self.conn.commit()
        self.conn.close()