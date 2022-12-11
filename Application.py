import sys
import func
from util.Calculator import *
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
            fileData, _ = QFileDialog.getOpenFileNames(parent=self, caption='Select a Data File', filter=file_filter,
                                                  options=QFileDialog.DontUseNativeDialog)
            self.colData.setText("1");

        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Please choose a data set!')
    def preprocess_data(self):
        if self.label_column.text() != '' and self.begin_col.text()!='' and self.begin_row.text() !='':
            colLabel = int(self.colLabelEdit.text()) -1
            colData = int(self.colDataEdit.text()) -1

            try:
                self.message = QtWidgets.QMessageBox()
                self.message.setText("Column "+ str(colLabel +1)+ " is label column ?")
                self.message.show()
                self.items, self.true_label = ReadData(fileData)

            except:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.showMessage('Please choose a column in range !')
    
    def caculate_cluster(self):
        if (self.numberClusterText.text() != '' 
            and self.epsilonText.text() != '' 
            and self.maxIterText.text() != ''):
            numberClusters = int(self.numberClusterText.text())
            Epsilon = float(self.epsilonText.text())
            maxIter = int(self.maxIterText.text())
            if (self.comboBox.getText() == "FCM"):
                try:
                    m = int(self.mText.text())
                    func.run_FCM(items, numberClusters, Epsilon, m, maxIter)
                except:
                    self.error_dialog = QtWidgets.QErrorMessage()
                    self.error_dialog.showMessage('Please fill all input of FCM!')
            elif (self.comboBox.getText() == "MC-FCM"):
                try:
                    mL = int(self.mLText.text())
                    mU = int(self.mUText.text())
                    alpha = int(self.alphaText.text())
                    func.run_MC_FCM()
                except:
                    self.error_dialog = QtWidgets.QErrorMessage()
                    self.error_dialog.showMessage('Please fill all input of MC-FCM!')
            elif (self.comboBox.getText() == "sSMC-FCM"):
                try:
                    M = int(self.MText.text())
                    M_ = int(self.M_Text.text())
                    rate = int(self.rateText.text())
                    func.run_sSMC_FCM()
                except:
                    self.error_dialog = QtWidgets.QErrorMessage()
                    self.error_dialog.showMessage('Please fill all input of sSMC-FCM!')
                    