import sys
import os
import smtplib, ssl
from datetime import datetime

from src.Logger.Logger import Logger

from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)

dotenv_path = os.path.join(ROOT_DIR, '.env')
load_dotenv(dotenv_path)

date = datetime.now().strftime("%d_%m_%Y_%H:%M")

class Mailer():
    def __init__(self):
        self.__port = os.environ.get('MAIL_PORT')
        self.__email = os.environ.get('MAIL_ADDRESS')
        self.__password = os.environ.get('MAIL_PASSWORD')
        self.__context = ssl.create_default_context()

    def send(self, body):
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', self.__port)
            server.ehlo()
            server.login(self.__email, self.__password)
            server.sendmail(self.__email, 'elvissabanovic3@gmail.com', body)
            server.close()
        except Exception as e:
            raise e