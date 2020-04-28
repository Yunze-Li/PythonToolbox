import smtplib
import sys


# A simple test to see if the gmail address SMTP service is setup successfully
def smtp_gmail_test(sender_address: str, sender_password: str):
    mail_host = "smtp.gmail.com"  # 设置服务器
    receivers = [sender_address]  # 接收邮件方
    message = "test_message"
    try:
        server = smtplib.SMTP_SSL(mail_host, 465)  # 465 为 SMTP 端口号
        server.ehlo()
        server.login(sender_address, sender_password)
        server.sendmail(sender_address, receivers, message)
        server.quit()
        print("邮件发送成功")
    except:
        print("无法发送邮件")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("输入有误, 请输入邮箱及密码")
    else:
        smtp_gmail_test(sys.argv[1], sys.argv[2])
