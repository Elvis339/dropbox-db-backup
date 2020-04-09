from src.Engineer.Engineer import Engineer
from datetime import datetime
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

from src.Mailer.Mailer import Mailer
from src.Logger.Logger import Logger

import sys
import os
from dotenv import load_dotenv
ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)
dotenv_path = os.path.join(ROOT_DIR, '.env')
load_dotenv(dotenv_path)

class Dropbox(Engineer):
    def __init__(self, dropbox_path):
        super().__init__()
        self.dropbox_path = dropbox_path
        self.__dbx = dropbox.Dropbox(os.environ.get('DROPBOX_TOKEN'))

    def __upload_file(self):
        name = datetime.now().strftime('%d_%m_%Y_%H:%M')
        with open(self.path, 'rb') as data:
            try:
                self.__dbx.files_upload(data.read(), self.dropbox_path, mode=WriteMode('overwrite'))
            except ApiError as err:
                raise err

    def upload(self):
        try:
            mailer = Mailer()
            logger = Logger()
            self.backup()
            self.__upload_file()
            self.remove_backup()
            mailer.send('Backup preformed successfully.')
        except Exception as e:
            logger.log(e)
            mailer.send('Backup was not uploaded to Dropbox, please check the logs!')
        finally:
            print('Executed')