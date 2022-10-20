import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime
#import time



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

    def setJson(self, url):
        page = requests.get(url)
        self.jsonDoc = json.loads(page.text)

    def openYearData(self):
        data = ''
        with open('Data.txt', 'r', encoding='utf-8') as DataFile:
            data = DataFile.read()
            DataFile.close()

        self.jsonDoc = json.loads(data)
        self.size = len(self.jsonDoc)
        DTArray = np.zeros(self.size, dtype=datetime)
        self.DataFrame = pd.DataFrame({'DateTime' : DTArray})

    def Parse(self):
        i = 0

        for TimeData in self.jsonDoc:
            if i%100 == 0:
                print(i, end='  ')
            if i%2000 == 0 and i != 0:
                return

            if TimeData['uName'] == 'Тест воздуха':
                #self.dataSet['DateTime'].append(TimeData['Date'])
                DateTime = datetime.strptime(TimeData['Date'], '%Y-%m-%d %H:%M:%S')
                self.DataFrame['DateTime'].iloc[i] = DateTime

                for key in TimeData['data']:
                    if 'CO2' in key:

                        if not(key in self.DataFrame.columns):
                            self.DataFrame[key] = np.zeros(self.size, dtype=float)
                            self.DataFrame[key].iloc[i] = TimeData['data'][key]
                        else:
                            self.DataFrame[key].iloc[i] = TimeData['data'][key]

                i += 1

    def ParseDay(self, today):
        yearMonth = today.year
        month = today.month
        day = today.day
        #self.DataFrame = pd.DataFrame({'DateTime':})

    def printDoc(self):
        if self.jsonDoc:
            for key in self.jsonDoc:
                print('Date: {a}; type={b}'.format(a=self.jsonDoc[key]['Date'], b=type(self.jsonDoc[key]['Date'])))
                print('uName: {a}; type={b}'.format(a=self.jsonDoc[key]['uName'], b=type(self.jsonDoc[key]['uName'])))
                print('serial: {a}; type={b}'.format(a=self.jsonDoc[key]['serial'], b=type(self.jsonDoc[key]['serial'])))
                print('data: {a}; type={b}'.format(a=self.jsonDoc[key]['data'], b=type(self.jsonDoc[key]['data'])))
                print('\n'+'-'*50+'\n')

if __name__=='__main__':
    parser = Parser()
    test_url = 'http://webrobo.mgul.ac.ru:3000/db_api_REST/not_calibr/log/2021-09-01%2000:00:00/2021-09-01%2023:59:59/'
    parser.setJson(test_url)
    print(type(parser.jsonDoc))
    parser.printDoc()
