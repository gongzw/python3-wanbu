#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/4/11


import os,sys
BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BaseDir)
sys.path.append(BaseDir)

import time
from modules import monitor,sendMsg
from modules import utils



slave_conf = utils.get_config('slave_config')
slave_ip_list = slave_conf["slave_host"].split(',')
print(slave_ip_list)


while True:
    #msgsend_flag = True
    send_count = 0
    last_msg = ''
    alarm_counter = {

    }

    for host in slave_ip_list:
        conf_dict = {
            'host' : host,
            'port' : int(slave_conf["slave_port"]),
            'user' : slave_conf["slave_user"],
            'passwd': slave_conf["slave_passwd"],
            'charset' : "utf8" ,

        }

        My_host = conf_dict['host']
        monitor_obj = monitor.MySQL_monitor(**conf_dict)
        if monitor_obj.isSlave():
            send_count = 0
            alarm_counter[My_host] = ('',send_count)
            print(alarm_counter)
        else:
            alarm_counter[My_host] = ('', send_count)
            msgsend = sendMsg.notify_sendmsg()
            for msg in monitor_obj.__error__:
                if msg == alarm_counter[My_host][0] and alarm_counter[My_host][0] <= 3:
                    msgsend.send_msg(msg)
                    send_count += 1
                    alarm_counter[My_host][1] = send_count
                else:
                    pass


    time.sleep(60)