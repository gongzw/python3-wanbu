#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/4/10

import os,sys
BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BaseDir)
sys.path.append(BaseDir)

import telnetlib
import pymysql
from modules import utils
from modules import api
from modules import logger


class notify_sendmsg(object):
    '''
    发送告警短信
    '''
    msg_conf = utils.get_config('msg_config')
    cmdb_conf = utils.get_config('cmdb_config')
    def __init__(self):
        self.__msg_config__ = {
            "host": self.msg_conf['msgdb_host'],
            "port": int(self.msg_conf['msgdb_port']),
            "user": self.msg_conf['msgdb_user'],
            "passwd": self.msg_conf['msgdb_passwd']
        }

        self.__cmdb_config__ = {
            "host": self.cmdb_conf['cmdb_host'],
            "port": int(self.cmdb_conf['cmdb_port']),
            "user": self.cmdb_conf['cmdb_user'],
            "passwd": self.cmdb_conf['cmdb_passwd'],
            "db": self.cmdb_conf['cmdb_dbname'],
            "charset": "utf8"

        }

    def send_msg(self,msg):
        '''
        发送告警短信
        :param msg:
        :return:
        '''
        print(self.__cmdb_config__)
        db_api_ExecQuery = api.db_handler_ExecQuery(self.__cmdb_config__)
        msg_receive_users = db_api_ExecQuery("select name,mobile from user where username != 'admin';")
        msg_receive_users = set(msg_receive_users)
        print(msg_receive_users)
        for user_tu in msg_receive_users:
            username = user_tu[0]
            phoneNu = user_tu[1]
            content_sql = "set names 'gbk';" + "\n" + "insert into ultrax.msgsend (service, srcNo,destNo,  msgcontent) values ('30','10000', {0}, '【万步网】 {1} ');".format(phoneNu,msg)
            content_sql = content_sql.encode('gbk')  # 需要重新编码
            #print(content_sql)
            try:
                db_api_ExecQuery_msg = api.db_handler_ExecNonQuery(self.__msg_config__)
                db_api_ExecQuery_msg(content_sql)
                logger.log_hander().debug("向用户 {0} 号码 {1} 发送短信 {2} 成功.".format(username,phoneNu,msg))

            except pymysql.Warning as w:    # 异常处理
                print ("Mysql Error  %s" % (w))

if __name__ == "__main__":
    opt = notify_sendmsg()
    status = opt.send_msg("slave is error...")