#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/4/8

import os,sys
BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BaseDir)
sys.path.append(BaseDir)

import telnetlib
import pymysql
from modules import utils
from modules import api
from modules import logger


class MySQL_monitor(object):
    '''
    监控Mysql状态
    '''
    __error__ = []
    cmdb_conf = utils.get_config('cmdb_config')

    def __init__(self,**kwargs):
        self.__config__ = kwargs
        self.__config__['cursorclass'] = pymysql.cursors.DictCursor
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.__cmdb_config__ = {
            "host": self.cmdb_conf['cmdb_host'],
            "port": int(self.cmdb_conf['cmdb_port']),
            "user": self.cmdb_conf['cmdb_user'],
            "passwd": self.cmdb_conf['cmdb_passwd'],
            "db": self.cmdb_conf['cmdb_dbname'],
            "charset": "utf8"

        }

    def telnet(self, host, port, timeout=5):
        """
        测试服务器地址和端口是否畅通
        :param host: 服务器地址
        :param port: 服务器端口
        :param timeout: 测试超时时间
        :return: Boolean
        """
        try:
            tel = telnetlib.Telnet(host, port, timeout)
            tel.close()
            return True
        except:
            return False

    def connect(self,type):
        """
        创建数据库连接
        :param type:  type分为查询类型ExecQuery和非查询类型NonExecQuery（增删改）
        :return:
        """
        try:
            if self.telnet(self.__config__["host"], self.__config__["port"]):
                print("\033[34;1m数据库连接成功！\033[0m")
                if type == 'ExecQuery':
                    db_api_ExecQuery = api.db_handler_ExecQuery(self.__config__)
                elif type == 'NonExecQuery':
                    db_api_ExecQuery = api.db_handler_NonExecQuery(self.__config__)

                return db_api_ExecQuery
            else:
                print("unable connect mysql server {0}:{1}".format(self.__config__["host"],self.__config__["port"]))
                self.__error__.append("unable connect mysql server {0}:{1}".format(self.__config__["host"],self.__config__["port"]))
                return False
                # raise Exception("unable connect mysql server {0}:{1}".format(self.__config__["host"],self.__config__["port"]))

        except:
            self.__error__.append("无法连接服务器主机: {0}:{1}".format(self.__config__["host"],self.__config__["port"]))
            logger.log_hander().error("无法连接服务器主机: {0}:{1}".format(self.__config__["host"], self.__config__["port"]))

            return False

    def isSlave(self):
        """
        数据库同步是否正常
        :return: None同步未开启,False同步中断,True同步正常
        """
        db_api_ExecQuery_slave = self.connect('ExecQuery')
        if db_api_ExecQuery_slave:
            result = db_api_ExecQuery_slave("SHOW SLAVE STATUS")
            print(result)
            if result:
                db_api_ExecNonQuery = api.db_handler_ExecNonQuery(self.__cmdb_config__)
                sql = "select * from seos_1.mysql_slave_status where host = '%s';" % self.host
                # print(sql)
                res = db_api_ExecQuery_slave(sql)
                if len(res) == 0:
                    sql = "insert into seos_1.mysql_slave_status (host,slave_status,delay_status,alarm_count) values ('%s',1,1,0);" % self.host
                    # print(sql)
                    db_api_ExecNonQuery(sql)

                if result[0]["Slave_SQL_Running"] == "Yes" and result[0]["Slave_IO_Running"] == "Yes":
                    if result[0]["Seconds_Behind_Master"] >= 100:
                        print("\033[31;1m The slave is delay over 100s...\033[0m")
                        sql = "update seos_1.mysql_slave_status set delay_status=0 where host ='%s';" % self.host
                        db_api_ExecNonQuery(sql)
                        self.__error__.append("The Mysql slave {0}:{1} is delay over 100s...".format(self.__config__[\
                            "host"], self.__config__["port"]))
                        logger.log_hander().warn("The Mysql slave {0}:{1} is delay over 100s...".format(self.__config__[\
                            "host"], self.__config__["port"]))
                        return False
                    else:
                        print("\033[32;1m slave is ok...\033[0m")
                        sql = "update seos_1.mysql_slave_status set slave_status=1 where host ='%s';" % self.host
                        db_api_ExecNonQuery(sql)
                        return True
                else:
                    if result[0]["Slave_SQL_Running"] == "No":
                        print("\033[31;1m slave is error...\033[0m")
                        sql = "update seos_1.mysql_slave_status set slave_status=0 where host ='%s';" % self.host
                        db_api_ExecNonQuery(sql)
                        self.__error__.append(result["Last_SQL_Error"])
                    else:
                        self.__error__.append(result["Last_IO_Error"])
                    return False



if __name__ == "__main__":

    opt = MySQL_monitor(user='root', passwd="Dascom123!@#", host="192.168.20.179", port=3306,charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    status = opt.isSlave()
