from datetime import datetime

class Logger():
    def __init__(self):
        self.__today = datetime.now().strftime('%d_%m_%Y_%H:%M')

    def log(self, data):
        try:
            data = str(f'{data} - CREATED ON: {self.__today}\n')
            with open('log.txt', 'a') as log:
                log.write(data)
                log.close()
        except OSError as e:
            raise e