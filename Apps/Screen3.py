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
        self.pushButton_7.clicked.connect(self.pushLabel)

        # Store value for display label
        self.dict = {0: 'Đầu ra : Độ đo hiệu năng',
                     1: "Đầu ra : U",
                     2: "Đầu ra : V",
                     3: "Đầu ra : Nhãn"}
        # Store value of iterator
        self.dict1 = [0, 0, 0]
        # Store VerticalHeaderLabels eval
        self.list1 =  ['Rand Index',
                       'Davies-Bouldin Index',
                       'PBM index',
                       'Alternative Silhouette Width Criterion',
                       'Mean accuracy']
        # Store VerticalHeaderLabels eval


    def loadData(self, data_table, tableWidget):
        max_row = len(data_table)
        max_col = len(data_table[0])
        tableWidget.setRowCount(max_row)
        tableWidget.setColumnCount(max_col)
        for row in range(max_row):
            for col in range(max_col):
                tableWidget.setItem(row, col, QTableWidgetItem(str(round(data_table[row][col], 9))))

    def loadData1(self, data_table, tableWidget):
        max_row = len(data_table)
        max_col = len(data_table[0])
        tableWidget.setRowCount(max_row)
        tableWidget.setColumnCount(max_col)
        for row in range(max_row):
            for col in range(max_col):
                tableWidget.setItem(row, col, QTableWidgetItem(str(data_table[row][col])))

    def loadDataFCM(self, fcm,scaler):
        self.loadData(fcm.evalList, self.table_fcm_eval)
        V = scaler.inverse_transform(fcm.V)
        self.loadData(V, self.table_fcm_V)
        self.loadData(fcm.U, self.table_fcm_U)
        self.loadData1(fcm.table_map, self.table_fcm_label)

        self.table_fcm_eval.setVerticalHeaderLabels(self.list1)
        self.table_fcm_eval.setHorizontalHeaderLabels(["Kết quả"])
        self.table_fcm_label.setHorizontalHeaderLabels(["Nhãn số", "Nhãn tương ứng"])

        self.dict1[0] = fcm.iterator

    def loadDataMCFCM(self, mc_fcm,scaler):
        self.loadData(mc_fcm.evalList, self.table_mc_eval)
        V = scaler.inverse_transform(mc_fcm.V)
        self.loadData(V, self.table_mc_V)
        self.loadData(mc_fcm.U, self.table_mc_U)
        self.loadData1(mc_fcm.table_map, self.table_mc_label)

        self.table_mc_eval.setVerticalHeaderLabels(self.list1)
        self.table_mc_eval.setHorizontalHeaderLabels(["Kết quả"])
        self.table_mc_label.setHorizontalHeaderLabels(["Nhãn số", "Nhãn tương ứng"])

        self.dict1[1] = mc_fcm.iterator

    def loadDatasSMC(self, ssmc_fcm,scaler):
        self.loadData(ssmc_fcm.evalList, self.table_ssmc_eval)
        V = scaler.inverse_transform(ssmc_fcm.V)
        self.loadData(V, self.table_ssmc_V)
        self.loadData(ssmc_fcm.U, self.table_ssmc_U)
        self.loadData1(ssmc_fcm.table_map, self.table_ssmc_label)

        self.table_ssmc_eval.setVerticalHeaderLabels(self.list1)
        self.table_ssmc_eval.setHorizontalHeaderLabels(["Kết quả"])
        self.table_ssmc_label.setHorizontalHeaderLabels(["Nhãn số", "Nhãn tương ứng"])


        self.dict1[2] = ssmc_fcm.iterator

    def pushFCM(self):
        self.label.setText("Thuật toán: FCM")
        self.label_3.setText("Số lần lặp: " + str(self.dict1[0]))
        self.stackedWidget.setCurrentIndex(0)
        index = self.stackWidget_fcm.currentIndex()
        self.label_2.setText(self.dict[index])

    def pushMCFCM(self):
        self.label.setText("Thuật toán: MC-FCM")
        self.label_3.setText("Số lần lặp: " + str(self.dict1[1]))
        self.stackedWidget.setCurrentIndex(1)
        index = self.stackWidget_mc.currentIndex()
        self.label_2.setText(self.dict[index])

    def pushsSMC(self):
        self.label.setText("Thuật toán: sSMC-FCM")
        self.label_3.setText("Số lần lặp: " + str(self.dict1[2]))
        self.stackedWidget.setCurrentIndex(2)
        index = self.stackWidget_ssmc.currentIndex()
        self.label_2.setText(self.dict[index])

    def pushEval(self):
        self.label_2.setText(self.dict[0])
        widget = self.stackedWidget.currentIndex()
        if widget == 0:
            self.stackWidget_fcm.setCurrentWidget(self.page_fcm_eval)
        if widget == 1:
            self.stackWidget_mc.setCurrentWidget(self.page_mc_eval)
        if widget == 2:
            self.stackWidget_ssmc.setCurrentWidget(self.page_ssmc_eval)

    def pushU(self):
        self.label_2.setText(self.dict[1])
        widget = self.stackedWidget.currentIndex()
        if widget == 0:
            self.stackWidget_fcm.setCurrentWidget(self.page_fcm_U)
        elif widget == 1:
            self.stackWidget_mc.setCurrentWidget(self.page_mc_U)
        elif widget == 2:
            self.stackWidget_ssmc.setCurrentWidget(self.page_ssmc_U)

    def pushV(self):
        self.label_2.setText(self.dict[2])
        widget = self.stackedWidget.currentIndex()
        if widget == 0:
            self.stackWidget_fcm.setCurrentWidget(self.page_fcm_V)
        elif widget == 1:
            self.stackWidget_mc.setCurrentWidget(self.page_mc_V)
        elif widget == 2:
            self.stackWidget_ssmc.setCurrentWidget(self.page_ssmc_V)

    def pushLabel(self):
        self.label_2.setText(self.dict[3])
        widget = self.stackedWidget.currentIndex()
        if widget == 0:
            self.stackWidget_fcm.setCurrentWidget(self.page_fcm_label)
        elif widget == 1:
            self.stackWidget_mc.setCurrentWidget(self.page_mc_label)
        elif widget == 2:
            self.stackWidget_ssmc.setCurrentWidget(self.page_ssmc_label)
