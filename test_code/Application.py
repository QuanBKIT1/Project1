import sys

import numpy as np

import util.ProcessorData
from Cluster_Algorithm import FCM, MC_FCM, sSMC_FCM
from util.Calculator import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from TableUI1 import TableUI1
from TableUI2 import TableUI2

class MyWindowClass(QMainWindow):

    def __init__(self):
        super(MyWindowClass, self).__init__()
        uic.loadUi("../designer/Project1_UI.ui", self)
        #     test code
        self.dataPath.setText("C:/Users/Quan/iris.data")
        self.colLabelText.setText("4")
        self.colRText.setText("")
        self.numberClusterText.setText('3')
        self.epsilonText.setText('0.00001')
        self.maxIterText.setText('150')
        self.mText.setText('2')

    def viewData(self):
        try:
            data_table = readData(self.dataPath.text())
            self.Form = QtWidgets.QWidget()
            ui = TableUI1()
            ui.setupUi(self.Form)
            ui.loadData(data_table)
            self.Form.showMaximized()
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Đường dẫn không hợp lệ!')

    def choose_data(self):
        try:
            file_filter = 'Data File (*.xlsx *.csv *.data);; Excel File (*.xlsx *.xls)'
            path, _ = QFileDialog.getOpenFileName(parent=self, caption='Select a Data File', filter=file_filter,
                                                  options=QFileDialog.DontUseNativeDialog)
            self.dataPath.setText(path)

        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Please choose a data set!')

    def checkColumn(self):
        try:
            if self.colLabelText.text() != '':
                if self.colRText.text() == '':
                    self.colRedundant = None
                else:
                    self.colRedundant = self.colRText.text().split(',')
                    self.colRedundant = np.array(self.colRedundant, dtype='int')
                    for i in range(len(self.colRedundant)):
                        self.colRedundant[i] -= 1

                self.colLabel = (int)(self.colLabelText.text()) - 1
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Điều chỉnh dữ liệu chưa hợp lệ!')

    def viewData2(self):
        self.checkColumn()
        print(1)
        try:
            data_table = util.ProcessorData.readData(self.dataPath.text())
            data_table1 = np.array([data_table[i][self.colLabel] for i in range(len(data_table))])
            data_table1 = data_table1.reshape(len(data_table1),1)

            if self.colRedundant is None:
                data_table2 = None
            else:
                data_table2 = []
                for i in range(len(data_table)):
                    data_table2.append([data_table[i][j] for j in self.colRedundant])
                data_table2 = np.array(data_table2)

            self.items, self.true_label = util.ProcessorData.preprocessData(data_table, self.colLabel,
                                                                            self.colRedundant)
            print(1)
            self.mainWindow = QtWidgets.QMainWindow()
            self.tableUI2 = TableUI2()
            self.tableUI2.setupUi(self.mainWindow)
            self.tableUI2.loadData(data_table1,data_table2,self.items)
            self.mainWindow.showMaximized()

        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Chọn đường dẫn và điều chỉnh dữ liệu chưa hợp lệ! ')


    def preprocess_data(self):
        """
        Preprocessing dataset by calculating final data and true label
        Precondition: Enter valid datapath, label and redundant column
        """
        self.checkColumn()
        try:
            data_table = util.ProcessorData.readData(self.dataPath.text())
            self.items, self.true_label = util.ProcessorData.preprocessData(data_table, self.colLabel,
                                                                            self.colRedundant)
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Chọn đường dẫn và điều chỉnh dữ liệu chưa hợp lệ! ')

        print(self.colRedundant)
        print(self.colLabel)

    def run(self):
        self.preprocess_data()
        if (self.numberClusterText.text() != ''
                and self.epsilonText.text() != ''
                and self.maxIterText.text() != ''):
            self.numberClusters = int(self.numberClusterText.text())
            self.Epsilon = float(self.epsilonText.text())
            self.maxIter = int(self.maxIterText.text())

            if self.comboBox.currentText() == "FCM":
                try:
                    self.m = int(self.mText.text())
                    self.fcm = FCM.FCM(self.items, self.true_label, self.numberClusters, self.m, self.Epsilon,
                                       self.maxIter)
                    # print(self.items, self.true_label, self.numberClusters, self.m, self.Epsilon, self.maxIter)
                    self.fcm.run()
                    self.fcm.printResult()

                except:
                    self.error_dialog = QtWidgets.QErrorMessage()
                    self.error_dialog.showMessage('Please fill all input of FCM!')

            # elif (self.comboBox.currentText() == "MC-FCM"):
            #     try:
            #         mL = float(self.mLText.text())
            #         mU = float(self.mUText.text())
            #         alpha1 = float(self.alphaText.text())
            #         self.mc_fcm.MC_FCM(numberClusters, Epsilon, mL, mU, alpha1, maxIter)
            #         self.mc_fcm.printResult()
            #     except:
            #         self.error_dialog = QtWidgets.QErrorMessage()
            #         self.error_dialog.showMessage('Please fill all input of MC-FCM!')
            # elif (self.comboBox.currentText() == "sSMC-FCM"):
            #     try:
            #         M = float(self.MText.text())
            #         M1 = float(self.M1Text.text())
            #         rate = float(self.rateText.text())
            #         alpha2 = float(self.alphaText2.text())
            #         self.ssmc_fcm.sSMC_FCM(numberClusters, Epsilon, M, M1, rate, alpha2, maxIter)
            #         self.ssmc_fcm.printResult()
            #     except:
            #         self.error_dialog = QtWidgets.QErrorMessage()
            #         self.error_dialog.showMessage('Please fill all input of sSMC-FCM!')
            # else:
            #     try:
            #         m = int(self.mText.text())
            #         mL = float(self.mLText.text())
            #         mU = float(self.mUText.text())
            #         alpha1 = float(self.alphaText.text())
            #         M = float(self.MText.text())
            #         M1 = float(self.M1Text.text())
            #         rate = float(self.rateText.text())
            #         alpha2 = float(self.alphaText2.text())
            #         self.fcm.FCM(numberClusters, Epsilon, m, maxIter)
            #         self.mc_fcm.MC_FCM(numberClusters, Epsilon, mL, mU, alpha1, maxIter)
            #         self.ssmc_fcm.sSMC_FCM(numberClusters, Epsilon, M, M1, rate, alpha2, maxIter)
            #         self.fcm.printResult()
            #         self.mc_fcm.printResult()
            #         self.ssmc_fcm.printResult()
            #     except:
            #         self.error_dialog = QtWidgets.QErrorMessage()
            #         self.error_dialog.showMessage('Please fill all input!')


if __name__ == '__main__':
    app = QApplication([])
    mainWindow = MyWindowClass()
    mainWindow.show()
    sys.exit(app.exec_())
