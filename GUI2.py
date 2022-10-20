from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1485, 866)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 15, 1481, 801))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.allWidgets = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.allWidgets.setContentsMargins(0, 0, 0, 0)
        self.allWidgets.setObjectName("allWidgets")

        # Лэйаут для области рисования графика
        self.matlayout = QtWidgets.QVBoxLayout()
        # self.matlayout.setContentsMargins(0, 0, 0, 0)
        self.matlayout.setObjectName("matlayout")
        self.allWidgets.addLayout(self.matlayout)

        self.ToolWidgets = QtWidgets.QVBoxLayout()
        self.ToolWidgets.setObjectName("ToolWidgets")

        self.Radio = QtWidgets.QHBoxLayout()
        self.Radio.setObjectName("Radio")

        self.JRadio = QtWidgets.QRadioButton(self.horizontalLayoutWidget)    #Радиокнопка для переключения в режим JSON
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.JRadio.sizePolicy().hasHeightForWidth())
        self.JRadio.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.JRadio.setFont(font)
        self.JRadio.setObjectName("JRadio")
        self.Radio.addWidget(self.JRadio)

        self.CRadio = QtWidgets.QRadioButton(self.horizontalLayoutWidget)      #Радиокнопка для переключения в режим CSV
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CRadio.sizePolicy().hasHeightForWidth())
        self.CRadio.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.CRadio.setFont(font)
        self.CRadio.setObjectName("CRadio")
        self.Radio.addWidget(self.CRadio)

        self.ToolWidgets.addLayout(self.Radio)

        self.begin = QtWidgets.QDateTimeEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.begin.sizePolicy().hasHeightForWidth())
        self.begin.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.begin.setFont(font)
        self.begin.setDisplayFormat('dd.MM.yyyy HH:mm:ss')
        self.begin.setObjectName("begin")
        self.ToolWidgets.addWidget(self.begin)

        self.end = QtWidgets.QDateTimeEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.end.sizePolicy().hasHeightForWidth())
        self.end.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.end.setFont(font)
        self.end.setDisplayFormat('dd.MM.yyyy HH:mm:ss')
        self.end.setObjectName("end")
        self.ToolWidgets.addWidget(self.end)

        self.ToolWidgets.addStretch(1)

        #Надпись для обозначения получения данных
        self.status = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(16)
        self.status.setFont(font)
        self.status.setObjectName("status")
        self.ToolWidgets.addWidget(self.status)

        # ComboBox для выбора периодичности, за который строим график
        self.interval = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.interval.setObjectName("Interval");
        self.interval.addItem("Interval")
        self.interval.addItem("Second")
        self.interval.addItem("Minute")
        self.interval.addItem("Hour")
        self.ToolWidgets.addWidget(self.interval)

        self.sensor = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.sensor.setObjectName("Sensor")
        self.sensor.addItem("Sensor")
        self.ToolWidgets.addWidget(self.sensor)

        self.ToolWidgets.addStretch(2)

        '''
        self.CSVList = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.CSVList.setObjectName("CSVList")
        self.CSVList.setMaximumWidth(300)
        self.CSVList.setColumnCount(0)
        self.CSVList.setRowCount(0)
        self.CSVList.setColumnCount(1)
        self.CSVList.setRowCount(30)
        header = self.CSVList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.curRow = 0
        self.ToolWidgets.addWidget(self.CSVList)
        '''

        self.GetData = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.GetData.setFont(font)
        self.GetData.setObjectName("GetData")
        self.GetData.setMaximumWidth(300)

        self.DrButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.DrButton.setFont(font)
        self.DrButton.setObjectName("DrButton")
        self.DrButton.setMaximumWidth(300)

        self.Reset = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Reset.setFont(font)
        self.Reset.setObjectName("Reset")
        self.Reset.setMaximumWidth(300)

        self.ToolWidgets.addWidget(self.GetData)
        self.ToolWidgets.addWidget(self.DrButton)
        self.ToolWidgets.addWidget(self.Reset)
        self.allWidgets.addLayout(self.ToolWidgets)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1485, 25))
        self.menubar.setObjectName("menubar")

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())

        self.dataTitle = []
        self.data = {}
        self.Days = []
        self.Weeks = []
        self.Months = []
        self.Halfs = []
        self.Years = []

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Air Control"))
        self.JRadio.setText(_translate("MainWindow", "JSON"))
        self.CRadio.setText(_translate("MainWindow", "CSV"))
        self.status.setText(_translate("MainWindow", "No data"))
        self.DrButton.setText(_translate("MainWindow", "Нарисовать"))
        self.Reset.setText(_translate("MainWindow", "Сбросить"))
        self.GetData.setText(_translate("MainWindow", "Получить данные"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.action.setText(_translate("MainWindow", "Открыть"))

    #Метод, устнавливающий имена CSV-файлов в таблицу

    '''
    def setCSVList(self, text):
        if text == 'Day':
            for i in range(len(self.Days)):
                self.CSVList.setItem(i, 0, QTableWidgetItem(self.Days[i]))
        elif text == 'Week':
            for i in range(len(self.Weeks)):
                self.CSVList.setItem(i, 0, QTableWidgetItem(self.Weeks[i]))
        elif text == 'Month':
            for i in range(len(self.Months)):
                self.CSVList.setItem(i, 0, QTableWidgetItem(self.Months[i]))
        elif text == '6 months':
            print('Do method which links DataFrmames')
        elif text == 'Year':
            print('Do method which links DataFrames')
    '''
