from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import uic


class Screen3(QtWidgets.QMainWindow):
    def __init__(self):
        super(Screen3, self).__init__()
        uic.loadUi("../designer/screen3.ui", self)
        self.pushButton.clicked.connect(self.pushFCM)
        self.pushButton_2.clicked.connect(self.pushMCFCM)
        self.pushButton_3.clicked.connect(self.pushsSMC)
        self.pushButton_4.clicked.connect(self.pushEval)
        self.pushButton_5.clicked.connect(self.pushU)
        self.pushButton_6.clicked.connect(self.pushV)
        self.dict = {0:'Đầu ra : Độ đo hiệu năng',
                     1:"Đầu ra : U",
                     2:"Đầu ra : V"}

    def loadData(self, data_table, tableWidget):
        max_row = len(data_table)
        max_col = len(data_table[0])
        tableWidget.setRowCount(max_row)
        tableWidget.setColumnCount(max_col)
        for row in range(max_row):
            for col in range(max_col):
                tableWidget.setItem(row, col, QTableWidgetItem(str(round(data_table[row][col], 9))))

    def loadDataFCM(self, U, V, evalList):
        self.loadData(U, self.table_fcm_U)
        self.loadData(V, self.table_fcm_V)
        self.loadData(evalList, self.table_fcm_eval)
        self.table_fcm_eval.setVerticalHeaderLabels(['Rand Index',
                                                     'Davies-Bouldin Index',
                                                     'PBM index',
                                                     'Alternative Silhouette Width Criterion',
                                                     'Mean accuracy'])

    def loadDataMCFCM(self, U, V, evalList):
        self.loadData(U, self.table_mc_U)
        self.loadData(V, self.table_mc_V)
        self.loadData(evalList, self.table_mc_eval)
        self.table_mc_eval.setVerticalHeaderLabels(['Rand Index',
                                                     'Davies-Bouldin Index',
                                                     'PBM index',
                                                     'Alternative Silhouette Width Criterion',
                                                     'Mean accuracy'])

    def loadDatasSMC(self, U, V, evalList):
        self.loadData(U, self.table_ssmc_U)
        self.loadData(V, self.table_ssmc_V)
        self.loadData(evalList, self.table_ssmc_eval)
        self.table_ssmc_eval.setVerticalHeaderLabels(['Rand Index',
                                                     'Davies-Bouldin Index',
                                                     'PBM index',
                                                     'Alternative Silhouette Width Criterion',
                                                     'Mean accuracy'])

    def pushFCM(self):
        self.label.setText("Thuật toán: FCM")
        self.stackedWidget.setCurrentIndex(0)
        index = self.stackWidget_fcm.currentIndex()
        self.label_2.setText(self.dict[index])


    def pushMCFCM(self):
        self.label.setText("Thuật toán: MC-FCM")
        self.stackedWidget.setCurrentIndex(1)
        index = self.stackWidget_mc.currentIndex()
        self.label_2.setText(self.dict[index])

    def pushsSMC(self):
        self.label.setText("Thuật toán: sSMC-FCM")
        self.stackedWidget.setCurrentIndex(2)
        index = self.stackWidget_ssmc.currentIndex()
        self.label_2.setText(self.dict[index])

    def pushEval(self):
        self.label_2.setText(self.dict[0])
        widget = self.stackedWidget.currentIndex()
        if widget == 0:
            self.stackWidget_fcm.setCurrentWidget(self.page_fcm_eval)
            print('E')
        if widget == 1:
            self.stackWidget_mc.setCurrentWidget(self.page_mc_eval)
        if widget == 2:
            self.stackWidget_ssmc.setCurrentWidget(self.page_ssmc_eval)

    def pushU(self):
        self.label_2.setText(self.dict[1])
        widget = self.stackedWidget.currentIndex()
        if widget == 0:
            self.stackWidget_fcm.setCurrentWidget(self.page_fcm_U)
            print('U')
        elif widget == 1:
            self.stackWidget_mc.setCurrentWidget(self.page_mc_U)
        elif widget == 2:
            self.stackWidget_ssmc.setCurrentWidget(self.page_ssmc_U)

    def pushV(self):
        self.label_2.setText(self.dict[2])
        widget = self.stackedWidget.currentIndex()
        if widget == 0:
            self.stackWidget_fcm.setCurrentWidget(self.page_fcm_V)
            print('V')
        elif widget == 1:
            self.stackWidget_mc.setCurrentWidget(self.page_mc_V)
        elif widget == 2:
            self.stackWidget_ssmc.setCurrentWidget(self.page_ssmc_V)

