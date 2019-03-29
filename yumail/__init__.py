import ssl
from smtplib import SMTP, SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


email_servers = {
    "163.com": {"smtp": {"host": "smtp.163.com", "port": 25, "ssl_port": 465}},
}

context = ssl.create_default_context()


def parse_mail(mailname):

    server_name = mailname.split('@')

    if len(server_name) == 1:
        raise TypeError('email format error')

    server_name = server_name[-1]

    if server_name not in list(email_servers.keys()):
        raise NameError('No this email server')

    server = email_servers.get(server_name, '')
    return server


class Mail(SMTP):

    def __init__(self, mailname, pwd):
        self.mailname = mailname
        self.server = parse_mail(mailname).get('smtp', '')
        super().__init__(self.server.get('host'), self.server.get('port'))
        self.login(mailname, pwd)

    def send_text_mail(self, to, msg, subject=""):
        msg = self.mail_msg(msg, type='plain', subject=subject)
        return self.sendmail(self.mailname, to, msg)

    def send_html_mail(self, to, html_msg, subject=""):
        msg = self.mail_msg(html_msg, type='html', subject=subject)
        return self.sendmail(self.mailname, to, msg.as_string())

    def mail_msg(self, msg, type='plain', subject=""):
        msg = MIMEText(msg, type)
        msg['Subject'] = subject
        return msg

    def send_mail(self, to, msg, files=None, type='plain', subject=''):
        """Main function of send email.

        :param to : to address
        :param msg: message of string to send
        :param files: attachments
        :param type: format
        :param subject:
        """
        total = MIMEMultipart()
        total["Subject"] = subject

        body = self.mail_msg(msg, type=type, subject=subject)
        total.attach(body)

        if files and isinstance(files, list):
            for filename in files:
                file = MIMEApplication(open(filename, 'rb').read())
                file.add_header('Content-Disposition', 'attachment', filename=filename)
                total.attach(file)

        return self.sendmail(self.mailname, to, total.as_string())


class MailSSL(SMTP_SSL, Mail):
    """SSL sender"""

    def __init__(self, mail_name, pwd):
        self.mailname = mail_name
        server = parse_mail(mail_name).get('smtp', '')

        super().__init__(server.get('host'), server.get('ssl_port'))
        super().login(mail_name, pwd)



