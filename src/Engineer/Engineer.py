import os
import sys
from os import path
from datetime import datetime
from zipfile import ZipFile

import pexpect
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)

dotenv_path = path.join(ROOT_DIR, '.env')
load_dotenv(dotenv_path)


class Engineer():
    def __init__(self):
        self.__DB_USER = os.environ.get('DB_USER')
        self.__DB_PASSWORD = os.environ.get('DB_PASSWORD')
        self.__DB_NAME = os.environ.get('DB_NAME')
        self.__DB_HOST = os.environ.get('DB_HOST')
        self.__DB_PORT = os.environ.get('DB_PORT') or 3306
        self.path = self.__set_path()

    def __set_path(self, extension='.sql'):
        current_directory = os.getcwd()
        working_directory = path.join(current_directory, 'temp')
        backup_name_suffix = datetime.now().strftime('%d_%m_%Y_%H:%M')

        if not path.isdir(working_directory):
            os.makedirs(working_directory)
        backup_name = path.join(working_directory, backup_name_suffix)
        self.path = backup_name + extension
        return self.path

    def remove_backup(self):
        try:
            os.remove(self.path)
        except OSError as e:
            raise e


    def backup(self):
        try:
            command = f'mysqldum -h {self.__DB_HOST} -P {self.__DB_PORT} -u {self.__DB_USER} -p {self.__DB_NAME}'
            with open(self.path, 'wb') as file:
                child = pexpect.spawn(command)
                child.expect("Enter password: ")
                child.sendline(self.__DB_PASSWORD)
                data = child.read()
                child.wait()
                file.write(data)
        except Exception as e:
            raise e
