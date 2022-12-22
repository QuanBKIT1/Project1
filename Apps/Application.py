import sys
import util.ProcessorData
from Cluster_Algorithm import FCM, MC_FCM, sSMC_FCM
from Apps.fillData import fillData
from util.Calculator import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from Screen1 import Screen1
from Screen2 import Screen2
from Screen3 import Screen3


class MyWindowClass(QMainWindow):

    def __init__(self):
        super(MyWindowClass, self).__init__()
        uic.loadUi("../designer/Project1_UI.ui", self)
        #     test code
        self.fillData = fillData(self)
        self.fillData.fill_wine()

    def viewData(self):
        try:
            data_table = readData(self.dataPath.text())
            self.screen1 = Screen1()
            self.screen1.loadData(data_table)
            self.screen1.show()
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
        try:
            data_table = util.ProcessorData.readData(self.dataPath.text())
            data_table1 = np.array([data_table[i][self.colLabel] for i in range(len(data_table))])
            data_table1 = data_table1.reshape(len(data_table1), 1)

            if self.colRedundant is None:
                data_table2 = None
            else:
                data_table2 = []
                for i in range(len(data_table)):
                    data_table2.append([data_table[i][j] for j in self.colRedundant])
                data_table2 = np.array(data_table2)

            self.items, self.true_label = util.ProcessorData.preprocessData(data_table, self.colLabel,
                                                                            self.colRedundant)
            self.screen2 = Screen2()
            self.screen2.loadData(data_table1, data_table2, self.items)
            self.screen2.show()

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

    def run(self):
        """Action when press run"""
        self.runnable = 0
        if (self.numberClusterText.text() != ''
                and self.epsilonText.text() != ''
                and self.maxIterText.text() != ''):
            self.numberClusters = int(self.numberClusterText.text())
            try:
                self.Epsilon = float(self.epsilonText.text())
                self.maxIter = int(self.maxIterText.text())
                self.preprocess_data()
                self.runnable = 1
            except:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.showMessage('Đầu vào không hợp lệ')
        else:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Chưa nhập đủ giá trị các trường')
        try:
            if self.runnable == 1:
                algo = self.comboBox.currentText()
                self.screen3 = Screen3()
                if algo == "FCM":
                    self.runFCM()
                elif algo == "MC-FCM":
                    self.runMC_FCM()
                elif algo == "sSMC-FCM":
                    self.runsSMC_FCM()
                else:
                    self.runAll()
                self.screen3.show()
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Dữ liệu không hợp lệ (thiếu, sai số,...)')

    def runFCM(self):
        self.m = (float)(self.mText.text())
        fcm = FCM.FCM(self.items, self.true_label, self.numberClusters, self.m, self.Epsilon, self.maxIter)
        fcm.run()
        self.screen3.loadDataFCM(fcm.U, fcm.V, fcm.evalList)
        self.screen3.pushFCM()
        print("FCM running")

    def runMC_FCM(self):
        self.mL = (float)(self.mLText.text())
        self.mU = (float)(self.mUText.text())
        self.alpha = (float)(self.alphaText.text())
        mc_fcm = MC_FCM.MC_FCM(self.items, self.true_label, self.numberClusters, self.mL, self.mU, self.alpha,
                               self.Epsilon, self.maxIter)
        mc_fcm.run()
        self.screen3.loadDataMCFCM(mc_fcm.U, mc_fcm.V, mc_fcm.evalList)
        self.screen3.pushMCFCM()
        print("MC-FCM running")

    def runsSMC_FCM(self):
        self.M = float(self.MText.text())
        self.M1 = float(self.M1Text.text())
        self.alpha2 = float(self.alphaText2.text())
        self.rate = float(self.rateText.text())
        ssmc_fcm = sSMC_FCM.sSMC_FCM(self.items, self.true_label, self.numberClusters, self.M, self.M1,
                                     self.alpha2, self.rate, self.Epsilon, self.maxIter)
        ssmc_fcm.run()
        self.screen3.loadDatasSMC(ssmc_fcm.U, ssmc_fcm.V, ssmc_fcm.evalList)
        self.screen3.pushsSMC()
        print("sSMC running")

    def runAll(self):
        self.runFCM()
        self.runMC_FCM()
        self.runsSMC_FCM()


if __name__ == '__main__':
    app = QApplication([])
    mainWindow = MyWindowClass()
    mainWindow.show()
    sys.exit(app.exec_())
