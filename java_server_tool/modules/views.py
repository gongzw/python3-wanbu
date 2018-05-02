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
            script_path = info_dic[server_tag]['script_path']
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
            command = '%s start'%script_path
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
            script_path = info_dic[server_tag]['script_path']
            command = '%s start ' % script_path
            t = MyThread(execute_command, args=(hostname, username, command, server_tag,))
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
            CATALINA_HOME = info_dic[server_tag]['CATALINA_HOME']
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
        his_versions_dir = settings.DATABASE['roll_back_dir']
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
            CATALINA_HOME = info_dic[server_tag]['CATALINA_HOME']
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
        shutil.move("%s/%s"%(update_files_dir,service), his_versions_dir)
        os.chdir(his_versions_dir)
        now = time.strftime("%Y%m%d-%H%M")
        back_name = "%s.bak_%s"%(service,now)
        os.rename(service,back_name)
        #os.popen("rm -rf %s" % service)
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
            CATALINA_HOME = info_dic[server_tag]['CATALINA_HOME']
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
    if service == "all":
        sys.exit("\033[31;1m roll_back不支持all参数... \033[0m")
    else:
        roll_back_dir = settings.DATABASE['roll_back_dir']
        os.chdir(roll_back_dir)
        dir_list = os.listdir(roll_back_dir)
        if len(dir_list) == 0:
            sys.exit("\033[33;1m 没有可用的回滚版本...\033[0m")
        service_version_dic = {}
        print("\033[36;1m----------------------可用版本列表-------------------------\n\033\0m")
        for index,name in enumerate(dir_list):
            if name.split(".")[0] == service:
                index += 1
                service_version_dic[str(index)] = name
                print("%s:%s"%(index,name))
            else:
                sys.exit("\033[33;1m 没有可用的回滚版本...\033[0m")
        exit_flag = False
        while not exit_flag:
            choice_num = input("\033[35;1m\nChoice the %s version to rollback!(press 'q' to cancel)\n>>:\033[0m"%service).strip()
            if choice_num == "q" or choice_num == "Q":
                exit_flag = True

            elif choice_num not in service_version_dic:
                print("\033[31[1mInvalid Operation...\033[0m")
                continue

            else:
                rollBack_version = service_version_dic[choice_num]
                t_objs = []
                for server_tag in info_dic:
                    hostname = info_dic[server_tag]['hostname']
                    username = info_dic[server_tag]['username']
                    CATALINA_HOME = info_dic[server_tag]['CATALINA_HOME']
                    src_dir = rollBack_version
                    dest_dir = "%s/webapps" % CATALINA_HOME
                    # print("\033[34;1mserver_name：%s\033[0m" % server_tag)
                    command = "scp -r %s %s@%s:%s/" % (src_dir, username, hostname, dest_dir)
                    print("execute command:%s" % command)
                    t = MyThread(os.popen, args=(command,))
                    t.start()
                    t_objs.append(t)

                for t in t_objs:
                    t.join()

                restart(info_dic, service)
                os.popen("rm -rf %s" % service)
                print("\033[34;1m The  %s 回滚版本完成... \033" % service)
                exit_flag = True
