#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/1/19

import paramiko

def connect(host,username):
    'this is use the paramiko connect the host,return conn'
    private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
#        ssh.connect(host,username='root',allow_agent=True,look_for_keys=True)
        ssh.connect(hostname=host,username=username,pkey=private_key,allow_agent=True)
        return ssh
    except:
        return None

