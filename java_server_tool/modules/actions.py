#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/1/18

from conf import action_registers,settings
from modules import utils
import threading

json_file = "%s/%s"%(settings.DATABASE["path"],settings.DATABASE["name"])
server_info = utils.json_parser(json_file)

def choise_service():
    msg = u'''
    ---------选择操作的JAVA服务名称-----------
    \033[34;1m
    1.WanbuDataServer_NEW
    2.NEW_WAE_phone
    3.IMTE
    4.phoneServer
    5.JinSaiWebService
    6.dascom-java-socket-io-server
    7.JAVA_MODULE
    8.solr
    9.WanbuDataServer_TC
    \033[0m'''
    menu_dic = {
        "1":"WanbuDataServer_NEW",
        "2":"NEW_WAE_phone",
        "3":"IMTE",
        "4":"phoneServer",
        "5":"JinSaiWebService",
        "6":"dascom-java-socket-io-server",
        "7":"JAVA_MODULE",
        "8":"solr",
        "9":"WanbuDataServer_TC"
    }
    exit_flag = False
    while not exit_flag:
        print(msg)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            return menu_dic[user_option]

        else:
            print("\033[31;1mOption does not exist!\033[0m")


def choise_if_new():
    msg = u'''
    ---------选择操作的server连接的数据库-----------
    \033[34;1m
    1.连接旧DB的server
    2.连接新DB的server
    \033[0m'''
    menu_dic = {
        "1":"old",
        "2":"new"
    }
    exit_flag = False
    while not exit_flag:
        print(msg)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            return menu_dic[user_option]

        else:
            print("\033[31;1mOption does not exist!\033[0m")


def help_msg():
    '''
    print help msgs
    :return:
    '''
    print("\033[31;1mAvailable commands:\033[0m")
    for key in action_registers.actions:
        print("\t",key)
    msg = u'''
       ------- help info ---------
       \033[32;1m1.启动server：  start + "service or all"
       2.  停止模块：  stop + "service or all"
       3.  重启模块：  restart + "service or all"
       4.  查看模块启动状态： check_status + "service or all"
       5.  升级JAVA模块服务： update_service + "service"
       6.  更新JAVA模块配置： update_config + "service"
       7.  回滚JAVA模块服务： roll_back + “service"
       8.  帮助信息    help

       说明:1.使用参数"service"后会后续选择具体服务名称比如数据上传server（WanbuDataServer_NEW）
              选择后将对所有运行该server的tomcat进行操作
            2.使用参数"all"会对所有server进行操作
            3.升级、更新配置、回滚操作只能+service参数，不能用all
            4. 升级java模块时请将war包直接上传至java_server_tool/files 目录下，然后执行 ”python start.py update_service service“ 升级
            5. 修改配置文件时在模板目录：java_server_tool/templates 下进行修改   然后执行 ”python start.py update_config service“

       \033[0m'''
    print(msg)



def excute_from_command_line(argvs):
    service = None
    info_dic = server_info
    if len(argvs) < 2 or "help" in argvs:
        help_msg()
        exit()
    if argvs[1] not in action_registers.actions:
        utils.print_err("Command [%s] does not exist!" % argvs[1], quit=True)
    if "all" in argvs:
        service = 'all'
    if argvs[2] == "service":
        service = choise_service()
        server_dic = {}
        for server_tag in info_dic:
            hostname = info_dic[server_tag]['hostname']
            username = info_dic[server_tag]['username']
            service_dic = info_dic[server_tag]['service_name']
            CATALINA_HOME = "/home/%s/tomcat-new" % username
            script_file = settings.DATABASE["tomcat_script_name"]
            script_path = "/home/%s/tomcat-new/bin/%s" % (username, script_file)
            service_flag = 0  # 匹配service名称 默认值0 ，如果匹配结果则置为1
            for key in service_dic:
                if service == service_dic[key]:
                    service_flag = 1
                else:
                    continue
            if service_flag == 1:  # 匹配到service，执行命令
                server_dic[server_tag] = {'hostname':hostname,'username':username,'CATALINA_HOME':CATALINA_HOME,'script_path':script_path}
        info_dic = server_dic

    #print(info_dict)
    action_registers.actions[argvs[1]](info_dic,service)



