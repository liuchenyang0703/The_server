import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# 邮件配置
SMTP_SERVER = 'smtp.163.com'    # SMTP服务器的地址
SMTP_PORT = 465                 # SMTP服务器的SSL端口号
SMTP_USER = 'test@163.com'      # 发件人邮箱（用于登录）
SMTP_PASSWORD = '122222222222'  # 发件人邮箱SMTP授权码
SENDER = 'test@163.com'         # 发件人邮箱（用于发送）
RECIPIENTS = ['shoujianren123@qq.com'] # 收件人邮箱列表，多个可使用“,”分割；例如：['test1@qq.com','test2@qq.com']

def send_email(subject, content):
    """
    发送邮件告警
    :param subject: 邮件主题
    :param content: 邮件内容
    :return: 发送结果
    """
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = SENDER  # 直接使用发件人邮箱
        msg['To'] = ','.join(RECIPIENTS)  # 直接使用收件人邮箱列表
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 添加邮件正文
        msg.attach(MIMEText(content, 'html', 'utf-8'))
        
        # 连接SMTP服务器
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(0)
        
        # 登录SMTP服务器
        server.login(SMTP_USER, SMTP_PASSWORD)
        
        # 发送邮件
        server.sendmail(SENDER, RECIPIENTS, msg.as_string())
        
        # 关闭连接
        server.quit()
        
        return True
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        return False
