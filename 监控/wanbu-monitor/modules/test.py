#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Gongzw"
# Date: 2018/4/9

import telnetlib
import pymysql

class MySQL_monitor(object):
    '''
    监控Mysql状态
    '''

    __error__ = []

    def __init__(self,user,password,host,port):
        self.__config__ = {
            "user" :user,
            "password" :password,
            "host" :host,
            "port" :port,
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

    def connect(self):
        """
        创建数据库链接
        """
        try:
            if self.telnet(self.__config__["host"], self.__config__["port"]):
                print("\033[34;1m数据库连接成功！\033[0m")
                self.conn = pymysql.connect(host=self.__config__["host"],port=self.__config__["port"],\
                                            user=self.__config__["user"],passwd=self.__config__["password"],charset="utf8",cursorclass=pymysql.cursors.DictCursor)
                cur = self.conn.cursor()
                return cur
            else:
                raise Exception("unable connect")
        except:
            self.__error__.append("无法连接服务器主机: {host}:{port}".format(host=self.__config__[
                "host"], port=self.__config__["port"]))
            return False

    def isSlave(self):
        """
        数据库同步是否正常
        :return: None同步未开启,False同步中断,True同步正常
        """
        cur = self.connect()
        cur.execute("SHOW SLAVE STATUS;")
        result = cur.fetchone()
        cur.close()
        print(result)
        if result:
            if result["Slave_SQL_Running"] == "Yes" and result["Slave_IO_Running"] == "Yes":
                print("\033[32;1m slave is ok...\033[0m")
                return True
            elif result["Seconds_Behind_Master"] >= 100:
                print("\033[31;1m The slave is delay over 100s...\033[0m")
            else:
                if result["Slave_SQL_Running"] == "No":
                    print("\033[31;1m slave is error...\033[0m")
                    self.__error__.append(result["Last_SQL_Error"])
                else:
                    self.__error__.append(result["Last_IO_Error"])
                return False

    class notify_sendmsg(object):
        def __init__(self, config):
            self.config = config

        def ring(self, message=[]):
            subject = message.pop(0)
            messageBody = "".join(message)
            mailList = self.config["to"].split(";")
            datetime = time.strftime("%Y-%m-%d %H:%M:%S")
            for to in mailList:
                body = """
                <p>管理员<strong>{admin}</strong>，你好:</p>
                <p style="text-indent:2em;">收到这封邮件说明你的数据库同步出现异常，请您及时进行处理。</p>
                <p>异常信息：<br />{body}</p>
                <p style="text-align:right;">{date}</p>
                """.format(admin=to, body=messageBody, date=datetime)

                msg = MIMEText(body, "html", "utf-8")
                msg["From"] = self.config["from"]
                msg["To"] = to
                msg["Subject"] = subject
                smtp = smtplib.SMTP()

                smtp.connect(self.config["smtp_host"])
                if self.config.has_key("smtp_user"):
                    smtp.login(self.config["smtp_user"], self.config["smtp_password"])
                smtp.sendmail(self.config["from"], to, msg.as_string())
                smtp.quit()

if __name__ == "__main__":
    opt = MySQL_monitor("root","Dascom123!@#","192.168.20.179",3306)
    status = opt.isSlave()

