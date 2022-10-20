import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime

class BigCSV:
    def __init__(self):
        self.prib = {}
        self.DataFrame = None

    def addPribor(self, key):
        self.df = pd.read_csv(key+'.csv', sep=';', encoding='ISO-8859-1')
        dates = self.df['Date']
        datesPy = [datetime.strptime(moment, '%Y-%m-%d %H:%M:%S') for moment in dates]
        self.DataFrame = pd.DataFrame({'DateTime':datesPy})
        for column in self.df.columns:
            self.DataFrame[column] = self.df[column]


    def clear(self):
        if self.prib:
            self.prib.clear()
        if self.DataFrame:
            self.DataFrame = None

class Parser:
    def __init__(self):
        #self.dataSet = {'DateTime' : [], 'MH-Z14A_CO2': [], 'MHZ19B_CO2' : [], 'CCS811_eCO2' : []} #наборы данных для построения
        self.dataSet = {'DateTime' : []}

        self.DataFrame = None          #DataFrame с распарсенными значениями json
        self.jsonDoc = None            #json в python формате
        self.size = 0                  #количество строк в таблице

        self.averSpisoks = []   #список, который надо отсортировать

    def setJson(self, url):
        self.jsonDoc = requests.get(url)

    def ParseDay(self, *args):
        #Формируем запрос
        url = 'http://webrobo.mgul.ac.ru:3000/db_api_REST/not_calibr/log/'

        year = args[0]
        month = args[1]
        day = args[2]
        hour = args[3]
        minute = args[4]
        second = args[5]

        url += '{y0}-{mon0}-{d0}%20{h0}:{m0}:{s0}/'.format(y0=year[0], mon0=month[0], d0=day[0], h0=hour[0], m0=minute[0], s0=second[0])
        url += '{y}-{mon}-{d}%20{h}:{m}:{s}/'.format(y=year[1], mon=month[1], d=day[1], h=hour[1], m=minute[1], s=second[1])

        page = requests.get(url)

        if page.status_code == '404':
            raise ConnectionError          #Если не удалось получить данные за день, то кидаем исключение

        self.jsonDoc = json.loads(page.text)   #загружаем данные в словарь python

        #Считаем количество строк для DataFrame
        j = 0
        for moment in self.jsonDoc:
            if self.jsonDoc[moment]['uName'] == 'Тест воздуха':
                j+=1
        self.size = j
        DTArray = np.zeros(self.size, dtype=datetime)                #Массив DateTime
        self.DataFrame = pd.DataFrame({'DateTime': DTArray})

        notSortedDates = []
        SortedDates = []

        #Достаем данные из json и записываем их в DataFrame
        i = 0
        for moment in self.jsonDoc:
            if self.jsonDoc[moment]['uName'] == 'Тест воздуха':
                DateTime = datetime.strptime(self.jsonDoc[moment]['Date'], '%Y-%m-%d %H:%M:%S')
                newDict = {'DateTime':DateTime}

                for key in self.jsonDoc[moment]['data']:
                    if 'CO2' in key:

                        if not key in newDict:
                            newDict[key] = float(self.jsonDoc[moment]['data'][key])

                self.averSpisoks.append(newDict)

                i += 1

        sortedSpisok = self.QuickSort(self.averSpisoks)

        #добавляем колонки в DataFrame
        j = 0
        for key in self.averSpisoks[0]:
            if j!=0:
                array = np.zeros(self.size, dtype=float)
                self.DataFrame[key] = array
            j+=1

        for i in range(len(sortedSpisok)):
            for key in sortedSpisok[i]:
                self.DataFrame[key].iloc[i] = sortedSpisok[i][key]

    def PreParse(self, begin, end):

        # Форматируем в строку дату и время
        year, month, day, hour, minute, second = [], [], [], [], [], []
        
        year.append(str(begin.year))
        year.append(str(end.year))
        
        if begin.month < 10:
            month.append('0' + str(begin.month))
        else:
            month.append(str(begin.month))
            
        if end.month < 10:
            month.append('0' + str(end.month))
        else:
            month.append(str(end.month))

        if begin.day < 10:
            day.append('0' + str(begin.day)) 
        else:
            day.append(str(begin.day))
            
        if end.day < 10:
            day.append('0' + str(end.day)) 
        else:
            day.append(str(end.day))

        if begin.hour < 10:
            hour.append('0' + str(begin.hour))
        else:
            hour = str(begin.hour)
        
        if end.hour < 10:
            hour.append('0' + str(end.hour))
        else:
            hour.append(str(end.hour))
            
        if begin.minute < 10:
            minute.append('0' + str(begin.minute))
        else:
            minute.append(str(begin.minute))
            
        if end.minute < 10:
            minute.append('0' + str(end.minute))
        else:
            minute.append(str(end.minute))

        if begin.second < 10:
            second.append('0' + str(begin.second))
        else:
            second.append(str(begin.second))

        if end.second < 10:
            second.append('0' + str(end.second)) 
        else:
            second.append(str(end.second))

        self.ParseDay(year, month, day, hour, minute, second)

    #Быстрая сортировка для данных из json
    def QuickSort(self, spisok):
        opora = (0 + len(spisok)) // 2  # индекс опорного элемента

        leftSpisok = []   #для элементов меншье опорного
        rightSpisok = []  #для элементов больше опорного

        for i in range(len(spisok)):
            if i != opora:
                leftTime = spisok[i]['DateTime'].hour * 60 * 60 + spisok[i]['DateTime'].minute * 60 + spisok[i]['DateTime'].second
                oporaTime = spisok[opora]['DateTime'].hour * 60 * 60 + spisok[opora]['DateTime'].minute * 60 + spisok[opora]['DateTime'].second
                if leftTime < oporaTime:
                    leftSpisok.append(spisok[i])
                else:
                    rightSpisok.append(spisok[i])

        left = []
        right = []

        #Применяем сортировку для элементов, которые меньше опорного
        if len(leftSpisok) > 1:
            left = self.QuickSort(leftSpisok)
        elif len(leftSpisok) == 1:
            left = [leftSpisok[0]]

        #и для тех, которые больше опорного
        if len(rightSpisok) > 1:
            right = self.QuickSort(rightSpisok)
        elif len(rightSpisok) == 1:
            right = [rightSpisok[0]]

        #записываем результат
        res = []
        for i in range(len(left)):
            res.append(left[i])
        res.append(spisok[opora])
        for i in range(len(right)):
            res.append(right[i])

        return res


if __name__=='__main__':
    Big = BigCSV()
    Big.addPribor('september')  #Получаем DataFrane со значениями за месяц

    print('Count of rows: {a}'.format(a=Big.DataFrame.shape[0]))

    query = 'INSERT INTO teststudio_september(id, day, cur_time, '  #Начало запроса

    for i, column in enumerate(Big.DataFrame.columns):
        print('Big.DataFrame.columns{a} = {b}'.format(a=i, b=column))
    print('Big.DataFrame.columns{a} = {b}'.format(a=-2, b=column))
    print('-+'*40)

    #Добавляем в запрос имена колонок, которые будем изменять
    for i, column in enumerate(Big.DataFrame.columns):
        if column == 'DateTime' or column == 'Date':
            continue

        if i != 37:
            query += column + ', '
        elif i == 37:
            query += column + ')'
            break

    #Вставляем в запрос значения

    #id1 - id строки
    #day - день
    #times - время
    query += ' VALUES({a}, {b}, {c}'.format(a=id1, b=day, c=times)

    print(query)
'''
r'//home//naughtyfox//GraphicBuilder2//'+
'''
