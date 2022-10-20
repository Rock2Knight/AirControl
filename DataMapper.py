from datetime import datetime

import pandas as pd
import psycopg2
from psycopg2 import OperationalError

from schema import *
from parser_static import ParserStatic

query_id = 5001

#Коннектор между БД и парсером
class DataMapper:

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.result = ''

    #Функция для подключения к БД
    def create_connection(self, db_name, db_user, db_password, db_host, db_port):

        try:
            self.connection = psycopg2.connect(         #Подключаемся к БД
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            self.connection.autocommit = True
            print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            print(f"The error '{e}' occurred")

        self.cursor = self.connection.cursor()

    #Возвращаем список нужных полей для таблицы, которые есть в Series
    def get_existing_fields(self, series):
        atm_fields = ('BMP280_temp', 'BMP280_pressure', 'BMP280_humidity', 'BME280_temp', 'BME280_pressure', 'BME280_humidity', 'AM2321_temp', 'AM2321_humidity', 'AM1231_temp', 'AM1231_humidity')
        result_fields = list()

        for field in atm_fields:
            if field in series.index:
                result_fields.append(field)
        return result_fields

    #Запрос для вставки информации о давлении
    def create_info_query(self, table_name, data, day, cur_time, fields):
        global query_id

        query_left = 'INSERT INTO {tb_name}(id, day, cur_time, '.format(tb_name=table_name)
        length = len(fields)

        #Вставляем имена колонок
        for i in range(length):
            query_left = query_left + '{a}'.format(a=fields[i])
            if i != length-1:
                query_left = query_left + ', '
            else:
                query_left = query_left + ') VALUES ('

        query_aver = str(query_id) + ', ' + str(day) + ', \'' + cur_time + '\', '
        query_right = ''

        #Вставляем значения для строки
        for i in range(length):
            query_right = query_right + '{a}'.format(a=data[fields[i]])
            if i != length-1:
                query_right = query_right + ', '
            else:
                query_right = query_right + ');'

        raw_query = query_left + query_aver + query_right
        query_id += 1
        return raw_query

    #Метод для вставки строки
    def create_query(self, table_name, rows, values, day, cur_time):
        global query_id

        query_part1 = 'INSERT INTO {name}(id, day, cur_time, '.format(name=table_name)
        query_part2 = ' VALUES(' + str(query_id) + ', ' +  str(day) + ', \'' + str(cur_time) + '\', '

        #raw_query = 'INSERT INTO {name}(id, day, cur_time, '.format(name=table_name)
        #size_rows = len(rows)
        SQL_KEYS = SQL_NAMES.keys()

        #Удаление элементов, которые не нужны для таблицы
        del_index = list()
        for i in range(len(rows)):
            if rows[i] not in SQL_KEYS:
                del_index.append(i)
        for i in range(len(del_index)-1, -1, -1):
            rows.remove(rows[del_index[i]])
            values.remove(values[del_index[i]])

        size_rows = len(rows)

        #Подставляем в запрос имена колонок
        for i in range(size_rows):
            query_part1 = query_part1 + SQL_NAMES[rows[i]]
            if i != size_rows - 1:
                query_part1 = query_part1 + ', '
            else:
                query_part1 = query_part1 + ')'

        for i, value in enumerate(values):

            if rows[i] == 'RTC_date' or rows[i] == 'RTC_time':
                query_part2 = query_part2 + '\'' + value + '\''
            elif (rows[i] == 'BH1750_blink' or rows[i] == 'CCS811_ErrFlag') and value == '0':
                query_part2 = query_part2 + 'false'
            else:
                query_part2 = query_part2 + str(value)

            if i != len(values) - 1:
                query_part2 = query_part2 + ", "
            else:
                query_part2 = query_part2 + ");"

        raw_query = query_part1 + query_part2
        query_id += 1
        return raw_query

    #Исполнение запроса
    def insert_query(self, query):

        try:
            self.cursor.execute(query)
            print('Query with id[{id}] succesefully inserted'.format(id=query_id))

            #Вставляем данные о успешной работе запроса в лог-файл
            with open('query_log.txt', 'w', encoding='utf-8') as log:
                log.write('Query with id[{id}] succesefully inserted'.format(id=query_id))
                log.write('\n')

        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def select_id(self, id, column_name):
        query = 'SELECT {c} FROM TestStudio WHERE id={i};'.format(c=column_name, i=id)

        try:
            self.cursor.execute(query)
            self.result = self.cursor.fetchone()[0]
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        finally:
            self.cursor.close()

        return self.result

    def select_aver_per_day(self, day, column_name):
        query = 'SELECT {c} FROM TestStudio WHERE day={d}'.format(c=column_name, d=day)

        values = tuple()
        result = 0

        try:
            self.cursor.execute(query)
            values = self.cursor.fetchone()

            sum = 0
            for value in values:
                sum += value
            result = sum/len(values)

        except OperationalError as e:
            print(f"The error '{e}' occurred")
        finally:
            self.cursor.close()

        return result

    def destroy_connect(self):
        self.cursor.close()


if __name__ == '__main__':
    #Подключаемся к БД
    data_mapper = DataMapper()
    data_mapper.create_connection('testcruassan', 'cruassan', 'dragon', '127.0.0.1', '5432')

    #Парсим данные из json
    parser = ParserStatic()
    parser.parse_file('db_all_2021_05-06.json')
    parser.create_data_frames()


    print('Current data: {a}'.format(a=parser.moment_data[44124]['Date'].iloc[0]))

    stroka, day, month = parser.day_time(parser.moment_data[49124]['Date'].iloc[0])         #Формируем нужное нам представление дня и времени

    rows = list(parser.moment_data[49124].index)
    values = list(parser.moment_data[49124]['data'])
    data = pd.Series(values, rows)
    fields = data_mapper.get_existing_fields(data)

    query = data_mapper.create_info_query('teststudio_june', data, day, stroka, fields)

    '''
    for i in range(49123, 54123):
        stroka, day, month = parser.day_time(parser.moment_data[i]['Date'].iloc[0])         #Формируем нужное нам представление дня и времени

        rows = list(parser.moment_data[i].index)
        values = list(parser.moment_data[i]['data'])
        data = pd.Series(values, rows)
        fields = data_mapper.get_existing_fields(data)

        query = data_mapper.create_info_query('teststudio_june', data, day, stroka, fields)
        print(query)
        print('\n'+'--'*20+'\n')

        data_mapper.insert_query(query)
        print('\n'+'-+'*20+'\n');
    '''
