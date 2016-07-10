from email.mime.text import MIMEText
from smtplib import SMTP

__author__ = 'H.Rouhani'


class SmtpMail:
    host = None
    port = None
    user_name = None
    password = None

    def __init__(self, host, port, user_name=None, password=None):
        self.host = host
        self.port = port
        self.user_name = user_name
        self.password = password

    def send(self, sender, receivers, subject, content, message_type="plain"):
        """message_type could be plain, html, xml"""
        try:
            message = MIMEText(content, message_type)
            message['Subject']= subject
            smtp = SMTP(self.host, self.port)
            if self.user_name and self.password:
                smtp.login(self.user_name, self.password)
            smtp.sendmail(sender, receivers, message.as_string())
        except Exception as ex:
            raise ex
