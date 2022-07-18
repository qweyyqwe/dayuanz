# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : email.py
# @Software: PyCharm


import smtplib
from email.header import Header
from email.mime.text import MIMEText


class Sendmail(object):
    """
    发送邮件
    """
    def __init__(self, sender, password, receivers):
        self.sender = sender
        self.password = password
        self.receivers = receivers

    def send(self, ShowText, Name, Header_show):
        '''
        :param ShowText: 发送内容
        :param Name: 发送者
        :param Header_show: 发送文件抬头
        :return:
        '''
        message = MIMEText('%s' % (ShowText), 'plain', 'utf-8')
        message['From'] = Header("%s" % (Name), 'utf-8')
        message['To'] = Header(self.receivers)
        message['Subject'] = Header("%s" % (Header_show), 'utf-8')
        smtpObj = smtplib.SMTP('smtp.163.com')
        smtpObj.set_debuglevel(1)
        smtpObj.login(self.sender, self.password)
        smtpObj.sendmail(self.sender, self.receivers, message.as_string())
        smtpObj.quit()


