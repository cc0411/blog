#!/usr/bin/env python
# -*- coding:utf-8 -*-


import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def email(email_list, content, subject="恭喜你注册成功"):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(["xxx网站",'admin@jcwit.com'])
    msg['Subject'] = subject
    # SMTP服务
    server = smtplib.SMTP("mail@jcwit.com", 25)
    server.login("admin@jcwit.com", "xxxxx")
    server.sendmail('admin@jcwit.com', email_list, msg.as_string())
    server.quit()

