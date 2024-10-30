# coding:utf-8
import smtplib
import traceback

from email.mime.text import MIMEText
from email.header import Header

from config.basic_setting import SERVICE_MODE

test_email_info = {
    'mail_user': 'taeechn_test2@126.com',
    'mail_pass': 'VQMDFVPGVHQKJQJG',
    'sender': 'taeechn_test2@126.com'
    # password DGHOIGWRPGf12F
}

sub_type = {
    1: 'plain',
    2: 'html',
}


def send_email(receivers, cc, theme, email_content, email_type, email_service_info):
    receivers = list(set(receivers))
    cc = list(set(cc))
    if SERVICE_MODE in ['develop', 'testing']:
        receivers = ['dong.hu@zd-automotive.cn', 'extern.jianxin.xu@audi.com.cn']
        if "jun.liang@audi.com.cn" in receivers:
            receivers.remove("jun.liang@audi.com.cn")
            receivers.append('extern.jianxin.xu@audi.com.cn')
        if "qun.li@audi.com.cn" in receivers:
            receivers.remove("qun.li@audi.com.cn")
            receivers.append('dong.hu@zd-automotive.cn')
        cc = ["extern.yang.ma@audi.com.cn", "extern.jie.jiao@audi.com.cn", "extern.lan.gao@audi.com.cn",
              "extern.hao.lei@audi.com.cn", "extern.menghan.huang@audi.com.cn","yuxuan.li@audi.com.cn"]
    mail_host = 'smtp.126.com'
    email_info = test_email_info if SERVICE_MODE in ['develop', 'testing'] else email_service_info
    mail_user = email_info.get('mail_user')
    mail_pass = email_info.get('mail_pass')
    sender = email_info.get('sender')
    if len(receivers) == 0:
        receivers.append(sender)
    cc.append(sender)
    if sender and mail_user and mail_pass:
        message = MIMEText(email_content, sub_type.get(email_type), "utf-8")
        message["From"] = Header(sender)
        message["Subject"] = Header(theme, "utf-8")
        message["To"] = ';'.join(receivers)
        message["Cc"] = ';'.join(cc)
        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(mail_host, 25)
            smtp_obj.login(mail_user, mail_pass)
            all_receivers = receivers + cc
            smtp_obj.sendmail(sender, all_receivers, message.as_string())
        except smtplib.SMTPException as error:
            traceback.print_exc()
            print("send email error:{}".format(error))
