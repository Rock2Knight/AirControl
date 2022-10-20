#Программа для построения графика качества воздуха
from BigCSV import *

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QDateTimeEdit, QMessageBox

import matplotlib.dates
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from GUI2 import Ui_MainWindow

#Основной класс программы
class AirControl(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(AirControl, self).__init__()
        self.setupUi(self)
        self.addFigure()
        self.ser = None
        self.maxValue = 0
        self.maxValue1 = 0
        self.maxValue2 = 0

        self.xSet = []
        self.ySet = []
        self.parser = Parser()
        self.CSV = BigCSV()
        self.DataFrame = 0

        #Списки для CSV
        self.dataTitle = []
        self.data = {}
        self.Days = []
        self.Weeks = []
        self.Months = []
        self.Halfs = []
        self.Years = []

        #Флаги для отображения зон
        self.isPerfect = False
        self.isNormal = False
        self.isAccept = False
        self.isBad = False

        #self.CSVList.cellClicked.connect(self.chooseAver)
        self.GetData.clicked.connect(self.getData)
        self.DrButton.clicked.connect(self.writeData)   #При нажатии на кнопку рисования вызывается метод writeData
        self.Reset.clicked.connect(self.ClearGraph)     #При нажатии Reset стираем все с графика
        self.action.triggered.connect(self.getCSV)
        #self.period.activated[str].connect(self.setCSVList)

    #Метод, добавляющий область для рисования графика в GUI
    def addFigure(self):
        self.fig = Figure()  # Создаем область для фигуры
        self.axes = self.fig.add_subplot(111)  # Система координат
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        #Добавляем канву и меню навигации в виджет
        self.matlayout.addWidget(self.canvas)
        self.matlayout.addWidget(self.toolbar)

    #Метод, рисующий график
    def DrawGraph(self):
        titleOfSensor = ''
        colorScat = ''                                   #Цвет точек
        colorPlot = ''                                   #Цвет графика
        curLabel = ''                                    #Метка
        names = self.DataFrame.columns

        # Предупреждение об ошибке если не загрузили данные
        if not self.xSet and self.ySet:
            errorMessage = QMessageBox()
            errorMessage.setIcon(QMessageBox.Critical)
            errorMessage.setText("No graph data!")
            errorMessage.setInformativeText('No graph data')
            errorMessage.setWindowTitle("Where is Data!")
            errorMessage.exec_()
            return

        #Форматирование меток по оси X
        if len(self.DataFrame[names[0]]) > matplotlib.dates.HourLocator.MAXTICKS:
            self.axes.xaxis.set_major_locator(matplotlib.dates.HourLocator(interval=50))
        else:
            self.axes.xaxis.set_major_locator(matplotlib.dates.HourLocator())
        self.axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))

        # Прорисовка зон безопасности
        if self.maxValue <= 400:
            perfect = [400 for i in range(len(self.xSet))]
            if not self.isPerfect:
                self.axes.plot(self.xSet, perfect, color='green', linewidth=4, label='Отлично')
                self.isPerfect = True
        elif 400 < self.maxValue <= 800:
            if not self.isPerfect:
                perfect = [400 for i in range(len(self.xSet))]
                self.axes.plot(self.xSet, perfect, color='green', linewidth=4, label='Отлично')
                self.isPerfect = True
            if not self.isNormal:
                normal = [800 for i in range(len(self.xSet))]
                self.axes.plot(self.xSet, normal, color='olivedrab', linewidth=4, label='Нормально')
                self.isNormal = True
        elif 800 < self.maxValue <= 1000:
            if not self.isPerfect:
                perfect = [400 for i in range(len(self.xSet))]
                self.axes.plot(self.xSet, perfect, color='green', linewidth=4, label='Отлично')
                self.isPerfect = True
            if not self.isNormal:
                normal = [800 for i in range(len(self.xSet))]
                self.axes.plot(self.xSet, normal, color='olivedrab', linewidth=4, label='Нормально')
                self.isNormal = True
            if not self.isAccept:
                accept = [1000 for i in range(len(self.xSet))]
                self.axes.plot(self.xSet, accept, color='yellow', linewidth=4, label='Допустимо')
                self.isAccept = True
        elif self.maxValue > 1000:
            if not self.isPerfect:
                perfect = [400 for i in range(len(self.xSet))]
                self.axes.plot(self.xSet, perfect, color='green', linewidth=4, label='Отлично')
                self.isPerfect = True
            if not self.isNormal:
                normal = [800 for i in range(len(self.xSet))]
                self.axes.plot(self.xSet, normal, color='olivedrab', linewidth=4, label='Нормально')
                self.isNormal = True
            if not self.isAccept:
                accept = [1000 for i in range(len(self.xSet))]
                self.axes.plot(self.xSet, accept, color='yellow', linewidth=4, label='Допустимо')
                self.isAccept = True
            if not self.isBad:
                bad = [2500 for i in range(len(self.xSet))]
                self.axes.plot(self.xSet, bad, color='orange', linewidth=4, label='Плохо')

        #sensor1, sensor2 = names[2], names[3]
        sensor1, sensor2 = names[1], names[2]
        curText = self.sensor.currentText()

        #Настройка цвета графика
        if self.sensor.currentText() == names[1] or self.sensor.currentText() == names[2]:
            if self.interval.currentText() == 'Second':
                if curText == sensor1:
                    colorPlot = 'magenta'
                elif curText == sensor2:
                    colorPlot = 'blue'
                curLabel = self.sensor.currentText()
            elif self.interval.currentText() == 'Minute':
                colorScat = 'brown'
                colorPlot = 'deeppink'
                curLabel = self.sensor.currentText() + ' (по минутам)'
                self.axes.scatter(self.xSet, self.ySet, c=colorScat)
            elif self.interval.currentText() == 'Hour':
                colorScat = 'black'
                colorPlot = 'red'
                curLabel = self.sensor.currentText() + ' (по часам)'
                self.axes.scatter(self.xSet, self.ySet, c=colorScat)
        elif self.sensor.currentText() == names[1]:
            if self.interval.currentText() == 'Second':
                colorPlot = 'navy'
                curLabel = self.sensor.currentText()
            elif self.interval.currentText() == 'Minute':
                colorScat = '#000080'
                colorPlot = 'crimson'
                curLabel = self.sensor.currentText() + ' (по минутам)'
                self.axes.scatter(self.xSet, self.ySet, c=colorScat)
            elif self.interval.currentText() == 'Hour':
                colorScat = 'black'
                colorPlot = 'indigo'
                curLabel = self.sensor.currentText() + ' (по часам)'
                self.axes.scatter(self.xSet, self.ySet, c=colorScat)

        print('Type of X is {a}\nType of Y is {b}\n'.format(a=type(self.xSet[0]), b=type(self.ySet[0])))
        self.axes.plot(self.xSet, self.ySet, c=colorPlot, label=curLabel, linewidth=2)
        self.axes.set_ylabel('Концентрация углекислого газа, ppm', fontsize=16)
        self.axes.set_title('Концентрация CO2', fontsize = 14, color = 'red')
        self.axes.tick_params(axis='both', which='major', direction='inout', length=6, width=2, labelsize=14)
        self.fig.autofmt_xdate(rotation=90)                                        #Здесь вызывется ошибка при огромном количестве данных
        self.axes.grid(True, which='both')
        self.axes.legend(loc='upper right')
        self.canvas.draw()

    def ClearGraph(self):
        self.axes.clear()
        self.canvas.draw()
        self.isPerfect = False
        self.isNormal = False
        self.isAccept = False
        self.isBad = False

    def getCSV(self):
        # Получение имени файла и разделение его на имя и тип
        dialog = QtWidgets.QFileDialog()
        name = dialog.getOpenFileName(self.centralwidget)
        allfname = name[0]
        ind1, ind2 = 0, 0
        for i in range(len(allfname)):
            if i != 0 and allfname[-i] == '.':
                ind2 = -i
            if i != 0 and allfname[-i] == '/':
                ind1 = -i
                break
        Period = allfname[ind1 + 1:ind2]
        tip = allfname[ind2 + 1:]

        #Если при открыли не csv файл, выбрасываем исключение
        if tip != 'csv':
            message = QtWidgets.QMessageBox()
            message.setText('This file is not CSV! Try again')
            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = message.exec()
            return

        file = open(allfname, 'r')  # Открываем файл
        with file:
            data = file.read()  # Файл CSV
            izm = []  # Список названий столбцов в CSV файле
            d1 = 0
            for i in range(len(data)):
                if data[i] == ';':
                    sr = data[d1 + 1:i]
                    if sr[0] == '\n' or sr[:3] == '202':
                        break
                    else:
                        self.dataTitle.append(data[d1 + 1:i])
                        d1 = i

            # Корректировка izm
            st = ''
            if st in self.dataTitle:
                self.dataTitle.remove(st)
            if 'Date' in self.dataTitle:
                self.dataTitle.remove('Date')

            for el in self.dataTitle:
                if len(el) <= 7:
                    continue
                elif el[:7] == 'Unnamed':
                    self.dataTitle.remove(el)

            file.close()  # Закрываем файл

        #Добавляем названия датчиков
        self.sensor.clear()
        self.sensor.addItem('Sensor')
        for title in self.dataTitle:
            self.sensor.addItem(title)

        #Добавляем CSV в DataFrame
        self.CSV.clear()
        self.CSV.addPribor(Period)
        # fday = self.data[Period]['Date'].iloc[0]
        # day = fday[:10]
        # self.CSVList.setItem(self.curRow, 0, QTableWidgetItem(day))

    #Получаем данные
    def getData(self):
        today = datetime.today()

        dTE1 = self.begin.dateTime()
        lol1 = dTE1.toString("yyyy-MM-dd hh:mm:ss")
        DateTime1 = datetime.strptime(dTE1.toString("yyyy-MM-dd hh:mm:ss"), '%Y-%m-%d %H:%M:%S')
        dTE2 = self.end.dateTime()
        DateTime2 = datetime.strptime(dTE2.toString("yyyy-MM-dd hh:mm:ss"), '%Y-%m-%d %H:%M:%S')

        #Проверка на корректность даты
        if today.year != DateTime1.year or today.year != DateTime2.year:
            message = QtWidgets.QMessageBox()
            message.setText('Incorrect year')
            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = message.exec()
            return
        elif today.month != DateTime1.month or today.month != DateTime2.month:
            message = QtWidgets.QMessageBox()
            message.setText('Incorrect month')
            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = message.exec()
            return
        elif today.day != DateTime1.day or today.day != DateTime2.day:
            message = QtWidgets.QMessageBox()
            message.setText('Incorrect day')
            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = message.exec()
            return
        elif DateTime1.hour > DateTime2.hour:
            message = QtWidgets.QMessageBox()
            message.setText('Begin hour more than end hour')
            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = message.exec()
            return
        elif DateTime1.minute > DateTime2.minute:
            message = QtWidgets.QMessageBox()
            message.setText('Begin minute more than end minute')
            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = message.exec()
            return
        elif DateTime1.second > DateTime2.second:
            message = QtWidgets.QMessageBox()
            message.setText('Begin second more than end second')
            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = message.exec()
            return

        self.status.setText('Загрузка...')

        try:
            self.parser.PreParse(DateTime1, DateTime2)
        except ConnectionError:
            message = QtWidgets.QMessageBox()
            message.setText('404 Error')
            message.setInformativeText('Данные не получены в связи с проблемами связи. Попробуйте снова через некторое время')
            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = message.exec()
            return

        columns = self.parser.DataFrame.columns
        self.sensor.clear()
        self.sensor.addItem('Sensor')
        for i in range(len(columns)):
            if i!=0:
                self.sensor.addItem(columns[i])

        self.status.setText('Данные получены!')

    #Метод, подготавливающий списки для построения графика
    def writeData(self):
        if self.JRadio.isChecked():
            self.DataFrame = self.parser.DataFrame
        else:
            self.DataFrame = self.CSV.DataFrame

        if type(self.DataFrame)==type(0):
            message = QtWidgets.QMessageBox()
            message.setText('You did not open CSV!')
            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = message.exec()
            return

        sensor = self.sensor.currentText()

        if sensor == 'Sensor':
            message = QtWidgets.QMessageBox()
            message.setText('Sensor is not chosen')
            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = message.exec()
            return

        self.xSet.clear()
        self.ySet.clear()

        interval = self.interval.currentText()
        if interval == 'Interval':
            message = QtWidgets.QMessageBox()
            message.setText('Interval is not chosen')
            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = message.exec()
            return

        if interval == 'Second':
            for i in range(self.DataFrame.shape[0]):
                matDateTime = matplotlib.dates.date2num(self.DataFrame['DateTime'].iloc[i])  # преобразуем DateTime python в DateTime matplotlib
                self.xSet.append(matDateTime)
                yValue = float(self.DataFrame[sensor].iloc[i])
                self.ySet.append(yValue)


        elif interval == 'Minute':                                       #Делаем усреденение за минуту
            ySum = 0                   #Суммы показаний за минуту
            сount = 0                  #Количество показаний за минуту
            start = 0                  #Индекс с которого начинаем суммирование  (нужно для того, чтобы начать суммирование)
            i = 0                      #номер строки
            columns = self.DataFrame.columns  #получили имена колонок
            isChanged = False

            for i in range(self.DataFrame.shape[0]):
                if i == start or isChanged:
                    ySum = self.DataFrame[sensor].iloc[i]
                    count = 1
                    isChanged = False
                else:
                    hour_pr = self.DataFrame['DateTime'].iloc[i-1].hour
                    hour = self.DataFrame['DateTime'].iloc[i].hour
                    minute_pr = self.DataFrame['DateTime'].iloc[i-1].minute
                    minute = self.DataFrame['DateTime'].iloc[i].minute

                    if hour_pr == hour:                   #Если 1 и 2 время совпадают по часам и минутам
                        if minute_pr == minute:
                            ySum += self.DataFrame[sensor].iloc[i]         #Суммируем значения
                            count += 1                                            #Увеличиваем счетчик

                        else:
                            index = start + count // 2
                            matDateTime = matplotlib.dates.date2num(self.DataFrame['DateTime'].iloc[index])  # преобразуем DateTime python в DateTime matplotlib
                            # добавляем данные в списки   (*)
                            self.xSet.append(matDateTime)
                            self.ySet.append(ySum / count)

                            # Обнуляем сумму и счетчик
                            ySum = 0
                            count = 0
                            start = i
                            isChanged = True

                    else:
                        index = start + count // 2
                        matDateTime = matplotlib.dates.date2num(self.DataFrame['DateTime'].iloc[index])  # преобразуем DateTime python в DateTime matplotlib
                        # добавляем данные в списки   (*)
                        self.xSet.append(matDateTime)
                        try:
                            self.ySet.append(ySum / count)
                        except ZeroDivisionError:
                            message = QtWidgets.QMessageBox()
                            message.setText('Little data for this interval')
                            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
                            ret = message.exec()
                            return

                        # Обнуляем сумму и счетчик
                        ySum = 0
                        count = 0
                        start = i
                        isChanged = True

            if len(self.xSet) > len(self.ySet):
                spis = list(self.xSet)

                self.xSet.clear()
                for i in range(len(self.ySet)):
                    self.xSet.append(spis[i])

        elif interval == 'Hour':                                                    #Делаем усреденение за час
            ySum = 0                                 # Суммы показаний за минуту
            сount = 0                                # Количество показаний за минуту
            start = 0                                # Индекс с которого начинаем суммирование  (нужно для того, чтобы начать суммирование)
            i = 0                                    # номер строки
            columns = self.DataFrame.columns  # получили имена колонок
            dates = []

            for i in range(self.DataFrame.shape[0]):
                if i == start:
                    ySum = self.DataFrame[sensor].iloc[i]
                    count = 1
                else:
                    hour_pr = self.DataFrame['DateTime'].iloc[i-1].hour
                    hour = self.DataFrame['DateTime'].iloc[i].hour

                    if hour == hour_pr:
                        ySum += self.DataFrame[sensor].iloc[i]  # Суммируем значения
                        count += 1  # Увеличиваем счетчик
                    else:

                        index = start + count // 2
                        matDateTime = matplotlib.dates.date2num(self.DataFrame['DateTime'].iloc[index])  # преобразуем DateTime python в DateTime matplotlib
                        # добавляем данные в списки   (*)
                        try:
                            self.ySet.append(ySum / count)
                        except ZeroDivisionError:
                            message = QtWidgets.QMessageBox()
                            message.setText('Little data for this interval')
                            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
                            ret = message.exec()
                            return

                        self.xSet.append(matDateTime)

                        # Обнуляем сумму и счетчик
                        ySum = 0
                        count = 0
                        start = i

                dates.append(self.DataFrame['DateTime'].iloc[i])

            if len(self.xSet) > len(self.ySet):
                spis = list(self.xSet)

                self.xSet.clear()
                for i in range(len(self.ySet)):
                    self.xSet.append(spis[i])

        try:
            self.findMax()
        except:
            message = QtWidgets.QMessageBox()
            message.setText('No data in ySet')
            message.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = message.exec()
            return
        self.DrawGraph()              #Рисуем график

    def findMax(self):
        if not self.ySet:
            raise ValueError

        self.maxValue = 0
        for i in range(len(self.ySet)):
            if self.ySet[i] > self.maxValue:
                self.maxValue = self.ySet[i]
