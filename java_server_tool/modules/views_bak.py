#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/1/18

from modules.my_thread import MyThread
from modules import  ssh_create
from modules import utils
from conf import settings
import os,time,sys,shutil


def execute_command(hostname,username,command,server_tag):
    '''
    执行远程命令
    :return:
    '''
    ssh = ssh_create.connect(hostname,username)
    stdin, stdout, stderr = ssh.exec_command(command)
    res = stdout.read().decode()
    print(res)
    ssh.close()
    return server_tag,res

def action_operate(info_dic,service,command):
    '''
    接收action的命令并多线程远程执行
    :param info_dic:
    :param service:
    :param command:
    :return:
    '''
    pass

def stop(info_dic,service):
    '''
    停止模块
    :return:
    '''
    if service == "all":
        t_objs = []
        for server_tag in info_dic:
            hostname = info_dic[server_tag]['hostname']
            username = info_dic[server_tag]['username']
            script_file=settings.DATABASE["tomcat_script_name"]
            script_path = "/home/%s/tomcat-new/bin/%s" % (username, script_file)
            command = '%s stop'%script_path
            print("\033[34;1mserver_name：%s\033[0m" % server_tag)
            t = MyThread(execute_command, args=(hostname, username, command, server_tag,))
            t.start()
            t_objs.append(t)
        for t in t_objs:
            t.join()
    else:
        t_objs = []
        for server_tag in info_dic:
            hostname = info_dic[server_tag]['hostname']
            username = info_dic[server_tag]['username']
            service_dic = info_dic[server_tag]['service_name']
            script_file = settings.DATABASE["tomcat_script_name"]
            script_path = "/home/%s/tomcat-new/bin/%s" % (username, script_file)
            service_flag = 0     # 匹配service名称 默认值0 ，如果匹配结果则置为1
            for key in service_dic:
                if service == service_dic[key]:
                    service_flag = 1
                else:
                    continue
            if service_flag == 1:  # 匹配到service，执行命令
                command = '%s stop ' % script_path
                t = MyThread(execute_command, args=(hostname, username, command, server_tag,))
                t.start()
                t_objs.append(t)
            for t in t_objs:
                t.join()




def start(info_dic,service):
    '''
    启动模块
    :param m_info_tuple:
    :return:
    '''
    if service == "all":
        t_objs = []
        for server_tag in info_dic:
            hostname = info_dic[server_tag]['hostname']
            username = info_dic[server_tag]['username']
            script_file=settings.DATABASE["tomcat_script_name"]
            script_path = "/home/%s/tomcat-new/bin/%s" % (username, script_file)
            command = '%s start '%script_path
            print("\033[34;1mserver_name：%s\033[0m" % server_tag)
            t = MyThread(execute_command, args=(hostname, username, command, server_tag,))
            t.start()
            t_objs.append(t)
        for t in t_objs:
            t.join()
    else:
        t_objs = []
        for server_tag in info_dic:
            hostname = info_dic[server_tag]['hostname']
            username = info_dic[server_tag]['username']
            service_dic = info_dic[server_tag]['service_name']
            script_file = settings.DATABASE["tomcat_script_name"]
            script_path = "/home/%s/tomcat-new/bin/%s" % (username, script_file)
            service_flag = 0     # 匹配service名称 默认值0 ，如果匹配结果则置为1
            for key in service_dic:
                if service == service_dic[key]:
                    service_flag = 1
                else:
                    continue
            if service_flag == 1:  # 匹配到service，执行命令
                command = '%s start ' % script_path
                t = MyThread(execute_command, args=(hostname, username, command,server_tag,))
                t.start()
                t_objs.append(t)
            for t in t_objs:
                t.join()



def restart(info_dic,service):
    '''
    重启模块
    :return:
    '''
    stop(info_dic,service)
    time.sleep(1)
    start(info_dic,service)


def check_status(info_dic,service):
    '''
    查看模块状态
    :param m_info_tuple:
    :return:
    '''

    if service == "all":
        t_objs = []
        for server_tag in info_dic:
            hostname = info_dic[server_tag]['hostname']
            username = info_dic[server_tag]['username']
            CATALINA_HOME = "/home/%s/tomcat-new" % username
            command = 'ps -ef|egrep %s |egrep -v "grep"' % CATALINA_HOME
            print("\033[34;1mserver_name：%s\033[0m" % server_tag)
            t = MyThread(execute_command, args=(hostname, username, command,server_tag,))
            t.start()
            t_objs.append(t)

        for t in t_objs:
            t.join()
            res = t.get_result()
            if res[1]:
                print("\033[33;1m The Tomcat-%s is running... \033[0m"%res[0])
            else:
                print("\033[31;1m The Tomcat-%s was shutdown... \033[0m"%res[0])
    else:
        t_objs = []
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
                command = 'ps -ef|egrep %s |egrep -v "grep"' % CATALINA_HOME
                t = MyThread(execute_command, args=(hostname, username, command,server_tag,))
                t.start()
                t_objs.append(t)
        for t in t_objs:
            t.join()
            res = t.get_result()
            if res[1]:
                print("\033[33;1m The Tomcat-%s is running... \033[0m" % res[0])
            else:
                print("\033[31;1m The Tomcat-%s was shutdown... \033[0m" % res[0])


def update_service(info_dic,service):
    '''
    升级服务
    :param m_info_tuple:
    :return:
    '''
    if service == "all":
        sys.exit("\033[31;1m update_service不支持all参数... \033[0m")
    else:
        update_files_dir = settings.DATABASE['update_file_dir']
        update_file_path = "%s/%s.war" % (settings.DATABASE['update_file_dir'], service)
        config_files_path = "%s/%s" % (settings.DATABASE['config_file_dir'], service)
        if os.path.isfile(update_file_path):
            os.chdir(update_files_dir)
            print(os.getcwd())
            if os.path.exists("%s/%s" %(update_files_dir,service)):  # 判断升级的service文件是否存在，存在则删除
                os.popen("rm -rf %s"%service)
            #shutil.move(update_file_path, "%s/%s" %(update_files_dir,service))
            #os.chdir("%s/%s" %(update_files_dir,service))
            war_file_name = '%s.war'%service
            utils.un_zip(war_file_name) # 解压.war文件
            os.popen("rm -rf %s"%update_file_path)  # 删除.war文件
            os.popen("cp -r %s/* %s/%s/WEB-INF/classes/" % (config_files_path, update_files_dir, service))
        else:
            sys.exit("\033[31;1m The file %s is not exist... \033[0m" % update_file_path)

        t_objs = []
        for server_tag in info_dic:
            hostname = info_dic[server_tag]['hostname']
            username = info_dic[server_tag]['username']
            service_dic = info_dic[server_tag]['service_name']
            CATALINA_HOME = "/home/%s/tomcat-new" % username
            service_flag = 0  # 匹配service名称 默认值0 ，如果匹配结果则置为1
            for key in service_dic:
                if service == service_dic[key]:
                    service_flag = 1
                else:
                    continue
            if service_flag == 1:  # 匹配到service，执行命令
                src_dir = service
                dest_dir = "%s/webapps"%CATALINA_HOME
                #print("\033[34;1mserver_name：%s\033[0m" % server_tag)
                command = "scp -r %s %s@%s:%s/"%(src_dir,username,hostname,dest_dir)
                print("execute command:%s"%command)
                t = MyThread(os.popen, args=(command,))
                t.start()
                t_objs.append(t)

        for t in t_objs:
            t.join()

        restart(info_dic,service)
        os.popen("rm -rf %s" % service)
        print("\033[34;1m The  %s 升级完成... \033"%service)


def update_config(info_dic,service):
    '''
    更新配置文件
    :return:
    '''
    if service == "all":
        sys.exit("\033[31;1m update_config不支持all参数... \033[0m")
    else:
        config_files_path = "%s/%s" % (settings.DATABASE['config_file_dir'], service)
        if os.path.isdir(config_files_path):
            os.chdir(config_files_path)
        else:
            sys.exit("\033[31;1m The file %s is not exist... \033[0m" % config_files_path)

        t_objs = []
        for server_tag in info_dic:
            hostname = info_dic[server_tag]['hostname']
            username = info_dic[server_tag]['username']
            service_dic = info_dic[server_tag]['service_name']
            CATALINA_HOME = "/home/%s/tomcat-new" % username
            service_flag = 0  # 匹配service名称 默认值0 ，如果匹配结果则置为1
            for key in service_dic:
                if service == service_dic[key]:
                    service_flag = 1
                else:
                    continue
            if service_flag == 1:  # 匹配到service，执行命令

                src_dir = config_files_path
                dest_dir = "%s/webapps/%s/WEB-INF/classes" %(CATALINA_HOME,service)
                print("\033[34;1mserver_name：%s\033[0m" % server_tag)
                command = "scp -r %s/* %s@%s:%s/" % (src_dir, username, hostname, dest_dir)
                print("execute command:%s" % command)
                t = MyThread(os.popen, args=(command,))
                t.start()
                t_objs.append(t)

        for t in t_objs:
            t.join()

        restart(info_dic, service)
        print("\033[34;1m The  %s 配置修改完成... \033" % service)



def roll_back(info_dic,service):
    '''
    回滚
    :param info_dic:
    :param service:
    :return:
    '''
    pass
