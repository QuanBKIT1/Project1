from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow
from PyQt5 import uic


class Screen1(QtWidgets.QWidget):

    def __init__(self):
        super(Screen1, self).__init__()
        uic.loadUi("../designer/screen1.ui",self)

    def loadData(self, data_table):
        max_row = len(data_table)
        max_col = len(data_table[0])
        self.table.setRowCount(max_row)
        self.table.setColumnCount(max_col)
        for row in range(max_row):
            for col in range(max_col):
                self.table.setItem(row, col, QTableWidgetItem(str(data_table[row][col])))
