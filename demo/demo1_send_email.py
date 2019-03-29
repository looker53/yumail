from yumail import MailSSL

if __name__ == '__main__':

    msg = """
    This is a Demo.
    
    
    Over.
    
    Thanks.
    """

    with MailSSL('example@163.com', 'password') as mail:
        mail.send_mail('example@163.com', msg, subject="test")
