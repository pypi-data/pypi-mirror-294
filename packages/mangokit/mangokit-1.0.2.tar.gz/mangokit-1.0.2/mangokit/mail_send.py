# -*- coding: utf-8 -*-
# @Project: MangoServer
# @Description: 邮箱通知封装
# @Time   : 2022-11-04 22:05
# @Author : 毛鹏
import smtplib
from email.mime.text import MIMEText
from socket import gaierror

from mangokit.exceptions.error_msg import ERROR_MSG_0017
from mangokit.exceptions.tools_exception import SendMessageError


def mail_send(content: str) -> None:
    SendEmail().send_mail(content)


class SendEmail:

    def __init__(self):
        self.user_list = ['729164035@qq.com', ]
        self.send_user, self.email_host, self.stamp_key = '729164035@qq.com', 'smtp.qq.com', 'lqfzvjbpfcwtbecg'

    def send_mail(self, content: str, ) -> None:
        try:
            user = f"MangoTestPlatform <729164035@qq.com>"
            message = MIMEText(content, _subtype='plain', _charset='utf-8')  # MIMEText设置发送的内容
            message['Subject'] = f'【芒果测试平台服务运行通知】'  # 邮件的主题
            message['From'] = user  # 设置发送人 设置自己的邮箱
            message['To'] = ";".join(self.user_list)  # 设置收件人 to是收件人，可以是列表
            server = smtplib.SMTP()
            server.connect(self.email_host)
            server.login(self.send_user, self.stamp_key)  # 登录qq邮箱
            server.sendmail(user, self.user_list, message.as_string())  #
            server.close()
        except gaierror as error:
            raise SendMessageError(*ERROR_MSG_0017)

if __name__ == '__main__':
    mail_send('测试')