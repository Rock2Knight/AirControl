import json
from datetime import datetime

import pandas as pd

id = 0

#Класс для обработки данных из json, чтобы засунуть их в SQL-таблицу
class ParserStatic(object):
    def __init__(self):
        self.day = 0
        self.time = ''
        self.moment_data = list()    #Список DataFrame со значениями за конкретный момент времени
        self.json_data = dict()      #Словарь с распарсенными значениями в файле

    #Формирование словаря из json-документа
    def parse_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
            self.json_data = json.loads(text)

    #создание списка из DataFrame (данные за каждый момент времени)
    def create_data_frames(self):
        if not self.json_data:
            raise StopIteration

        for key, value in enumerate(self.json_data):
            if value['uName'] == 'Тест Студии':
                self.moment_data.append(pd.DataFrame(value))

    def day_time(self, timeString):
        hist_time = datetime.strptime(timeString, '%Y-%m-%d %H:%M:%S')

        hour, minute, second = '', '', ''
        if hist_time.hour < 10:
            hour = '0' + str(hist_time.hour)
        else:
            hour = str(hist_time.hour)

        if hist_time.minute < 10:
            minute = '0' + str(hist_time.minute)
        else:
            minute = str(hist_time.minute)

        if hist_time.second < 10:
            second = '0' + str(hist_time.second)
        else:
            second = str(hist_time.second)

        result = hour+':'+minute+':'+second

        return result, hist_time.day, hist_time.month

if __name__=='__main__':
    raw_data = dict()
    DataFrames = list()
    DTArray = None
    size = 0

    with open('db_all_2021_05-06.json', 'r', encoding='utf-8') as file:
        text = file.read()
        raw_data = json.loads(text)
        file.close()

    count = 0
    for key, value in enumerate(raw_data):
        if value['uName'] == 'Тест Студии':
            DataFrames.append(pd.DataFrame(value))
            count += 1

    print(DataFrames[0])
