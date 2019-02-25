#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/24 10:24
# @Author  : HT
# @Site    : 
# @File    : EMailsender.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues
from BaseModule.HTLogger import HTLogger
from BaseModule.Class import LazyProperty

import smtplib
from email.mime.text import MIMEText
from email.header import Header


MAIL_HOST = "smtp.163.com"
MAIL_USER = "18316551437@163.com"
MAIL_PASS = "Wobuzhidao0"

class Emailsender(HTLogger):
    def __init__(self):
        HTLogger.__init__(self, 'Email')


    def _get_smtper(self):
        try:
            stmper = smtplib.SMTP()
            stmper.connect(MAIL_HOST, 25)
            stmper.login(MAIL_USER, MAIL_PASS)
            return stmper
        except smtplib.SMTPServerDisconnected as error:
            self.logger.error('SMTP connection error:{}'.format(error))
            return None


    def send(self, contents, title, receivers=['18316551437@163.com']):
        '''

        :param contents: 数组类型
        :param title: 字符串
        :param receivers: 数组类型
        :return:
        '''

        sender = '18316551437@163.com'

        html_content = "<p>{}</p><ul>".format(title)
        for content in contents:
            html_content += "<li>{}</li>".format(str(content))
        html_content += "</ul>"

        message = MIMEText(html_content, 'html', 'utf-8')
        message['From'] = Header("BI部门", 'utf-8')
        message['To'] = Header("用户")
        subject = title
        message['Subject'] = Header(str(subject), 'utf-8')

        try:
            smtper = self._get_smtper()
            if smtper is None:
                return False
            smtper.sendmail(sender, receivers, message.as_string())
            self.logger.debug("邮件发送成功")
        except smtplib.SMTPRecipientsRefused or smtplib.SMTPRecipientsRefused as error:
            self.logger.error("无法发送邮件:{}".format(error))
            return False



if __name__ == '__main__':
    s = Emailsender()
    s.send( [152,15125,125152125,125125125,235], title='拼多多')