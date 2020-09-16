# coding: utf-8
import os
import sys
import time
import requests
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import json
from config import Config

if Config.ENABLE_PROXY:
    import socks
    import socket
    socks.set_default_proxy(socks.PROXY_TYPES[Config.PROXY_TYPE], Config.PROXY_IP, Config.PROXY_PORT)
    socket.socket = socks.socksocket


WIDTH = 50
SCREENSHOT_FILE = 'screenshot.jpg'

class SmtpPop3Base(object):
    def __init__(self):
        self.closed = True

    def login(self):
        self._login_impl()
        self.closed = False

    def assert_server_is_login(self, msg=None):
        if self.closed:
            msg = msg or '%s is not login' % self.__class__.__name__
            raise AssertionError(msg)

    def quit(self):
        if not self.closed:
            self._quit_impl()
            self.closed = True

    def _login_impl(self):
        raise NotImplementedError # virual function

    def _quit_impl(self):
        raise NotImplementedError # virual function


class SmtpServer(SmtpPop3Base):
    def __init__(self):
        super().__init__()
        self.from_addr = Config.USERNAME

    def _login_impl(self):
        if not Config.ENABLE_SSL:
            self.server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            self.server.set_debuglevel(Config.DEBUG_LEVEL)
        else:
            try:
                self.server = smtplib.SMTP_SSL(Config.SMTP_SERVER, Config.SMTP_PORT)
            except:
                self.server = smtplib.SMTP_SSL(Config.SMTP_SERVER)
            self.server.set_debuglevel(Config.DEBUG_LEVEL)
            self.server.ehlo(Config.SMTP_SERVER)

        self.server.login(Config.USERNAME, Config.PASSWORD)


    def _quit_impl(self):
        self.server.quit()

    def send_msg(self, to_addr, subject='', content=None, filename=None):
        self.assert_server_is_login()
        if not content:
            content = subject or '<EMPTY>'

        msg = MIMEText(content, 'plain', 'utf-8')

        if filename:
            multi_msg = MIMEMultipart()
            multi_msg.attach(msg)
            msg = multi_msg

            with open(filename, 'rb') as f:
                short_name = os.path.basename(filename)
                mime = MIMEBase('attachment', short_name.split('.')[-1], filename=short_name)
                mime.add_header('Content-Disposition', 'attachment', filename=filename)
                mime.add_header('Content-ID', '<0>')
                mime.add_header('X-Attachment-Id', '0')
                mime.set_payload(f.read())
                encoders.encode_base64(mime)
                msg.attach(mime)

        msg['From'] = self.from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject

        try:
            self.server.sendmail(self.from_addr, [to_addr], msg.as_string())
            print('Email sending to %s ... OK' % to_addr)
            return True
        except smtplib.SMTPException as e:
            print('Email sending to %s ... failed: <%s>.' % (to_addr,e))
            return False


class PopServer(SmtpPop3Base):
    def __init__(self):
        super().__init__()
        self.parser = Parser()
        self.login()

    def _login_impl(self):
        self.server = poplib.POP3(Config.POP_SERVER)
        self.server.set_debuglevel(Config.DEBUG_LEVEL)
        self.server.user(Config.USERNAME)
        self.server.pass_(Config.PASSWORD)

    def _quit_impl(self):
        self.server.quit()

    @property
    def msg_num(self):
        self.assert_server_is_login()
        return self.server.stat()[0]

    def get_msg(self, index):
        self.assert_server_is_login()
        __, lines, __ = self.server.retr(index)
        msg = b'\n'.join(lines).decode()
        msg = self.parser.parsestr(msg)
        return msg


class IpMonitor(object):
    IP_FILENAME = '__ip.txt'

    def __init__(self):
        self.smtp_server = SmtpServer()
        self.ip = self.load_ip()
    
    def load_ip(self):
        try:
            with open(self.IP_FILENAME, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ''

    def store_ip(self, ip):
        self.ip = ip
        with open(self.IP_FILENAME, 'w') as f:
            f.write(ip)


    def query_ip(self):
        r = requests.get('http://pv.sohu.com/cityjson?ie=utf-8')
        # return text is below:
        # 'var returnCitySN = {"cip": "115.192.37.116", "cid": "330100", "cname": "浙江省杭州市"};'
        if r.ok:
            s = r.text[r.text.find('{'):-1]
            obj = json.loads(s)
            return obj.get('cip')


    def send_email(self, to_addr, subject='', content=None, filename=None):
        try:
            self.smtp_server.login()
            self.smtp_server.send_msg(to_addr, subject, content, filename)
            self.smtp_server.quit()
            return True
        except:
            return False


    def run(self):
        while True:
            try:
                ip = self.query_ip()
                if ip and ip != self.ip and self.send_email(Config.RECIEVER, 'Ubuntu IP address: %s' % ip, ip):
                    self.store_ip(ip)
                time.sleep(Config.CHECK_INTERVAL*60)
            except KeyboardInterrupt:
                print('\nInterrupted by user.\nBye bye~~')
                break

if __name__ == "__main__":
    ip_monitor = IpMonitor()
    ip_monitor.run()
