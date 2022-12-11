import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from numpy.lib.npyio import NpzFile
from PyQt5 import uic

class MyWindowClass(QMainWindow):
    def __init__(self):
        super(MyWindowClass, self).__init__()
        uic.loadUi("designer/Project1_UI.ui", self)

    def choose_data(self):
        try:
            file_filter = 'Data File (*.xlsx *.csv *.data);; Excel File(*.xlsx *.xls)'
            path, _ = QFileDialog.getOpenFileNames(parent=self, caption='Select a Data File', filter=file_filter,
                                                  options=QFileDialog.DontUseNativeDialog)
            fileData = path
        #
        #
        #
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Please choose a data set!')
    def preprocess_data(self):
        if self.label_column.text() != '' and self.begin_col.text()!='' and self.begin_row.text() !='':
            colLabel = int(self.label_column.text()) -1
            beignCol = int(self.beginCol.text()) -1

            try:
                self.message = QtWidgets.QMessageBox()
                self.message.setText("Column "+ str(colLabel +1)+ " is label column ?")
                self.message.show()
                self.X_table.setModel(None)

            except:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.showMessage('Please choose a column in range !')

    def reset_view(self):
        self.