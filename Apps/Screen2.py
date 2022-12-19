from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow
from PyQt5 import uic


class Screen2(QMainWindow):
    def __init__(self):
        super(Screen2, self).__init__()
        uic.loadUi('../designer/screen2.ui', self)
        self.stackedWidget.setCurrentWidget(self.page)
        self.pushButton.clicked.connect(self.showTable1)
        self.pushButton_2.clicked.connect(self.showTable2)
        self.pushButton_3.clicked.connect(self.showTable3)

    def util_loadData(self, data_table, tableWidget):
        if data_table is None:
            return
        max_row = len(data_table)
        max_col = len(data_table[0])
        tableWidget.setRowCount(max_row)
        tableWidget.setColumnCount(max_col)
        for row in range(max_row):
            for col in range(max_col):
                tableWidget.setItem(row, col, QTableWidgetItem(str(data_table[row][col])))

    def loadData(self, data_table1, data_table2, data_table3):
        self.util_loadData(data_table1, self.tableWidget)
        self.util_loadData(data_table2, self.tableWidget_2)
        self.util_loadData(data_table3, self.tableWidget_3)

    def showTable1(self):
        self.stackedWidget.setCurrentWidget(self.page)

    def showTable2(self):
        self.stackedWidget.setCurrentWidget(self.page_2)

    def showTable3(self):
        self.stackedWidget.setCurrentWidget(self.page_5)
