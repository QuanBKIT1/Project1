import sys
from test_code import func
from Cluster_Algorithm import FCM, MC_FCM, sSMC_FCM
from util.Calculator import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from numpy.lib.npyio import NpzFile
from PyQt5 import uic

class MyWindowClass(QMainWindow):
    def __init__(self):
        super(MyWindowClass, self).__init__()
        uic.loadUi("../designer/Project1_UI.ui", self)
        self.fcm = FCM.FCM()
        self.mc_fcm = MC_FCM.MC_FCM()
        # self.ssmc_fcm = sSMC_FCM.sSMC_FCM()

    def choose_data(self):
        try:
            file_filter = 'Data File (*.xlsx *.csv *.data);; Excel File (*.xlsx *.xls)'
            path, _ = QFileDialog.getOpenFileName(parent=self, caption='Select a Data File', filter=file_filter,
                                                  options=QFileDialog.DontUseNativeDialog)
            self.dataPath.setText(path)
            self.colDataText.setText("1")
            self.fcm.setFileData(path)
            self.mc_fcm.setFileData(path)
            # self.ssmc_fcm.setFileData(path)

        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Please choose a data set!')
            
    def preprocess_data(self):
        if (self.colLabelText.text() != ''
            and self.colDataText.text()!=''):
            colLabel = int(self.colLabelText.text())
            colData = int(self.colDataText.text())

            try:
                self.fcm.processData(colLabel-1)
                self.mc_fcm.processData(colLabel-1)
                # self.ssmc_fcm.processData(colLabel-1)
                self.message = QtWidgets.QMessageBox()
                self.message.setText("Column "+ str(colLabel)+ " is label column ?")
                self.message.show()

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
            if (self.comboBox.currentText() == "FCM"):
                try:
                    m = int(self.mText.text())
                    self.fcm.FCM(numberClusters, Epsilon, m, maxIter)
                    self.fcm.printResult()
                    
                except:
                    self.error_dialog = QtWidgets.QErrorMessage()
                    self.error_dialog.showMessage('Please fill all input of FCM!')
                    
            elif (self.comboBox.currentText() == "MC-FCM"):
                try:
                    mL = float(self.mLText.text())
                    mU = float(self.mUText.text())
                    alpha = float(self.alphaText.text())
                    self.mc_fcm.MC_FCM(numberClusters, Epsilon, mL, mU, alpha, maxIter)
                    self.mc_fcm.printResult()
                except:
                    self.error_dialog = QtWidgets.QErrorMessage()
                    self.error_dialog.showMessage('Please fill all input of MC-FCM!')
            elif (self.comboBox.currentText() == "sSMC-FCM"):
                try:
                    M = int(self.MText.text())
                    M_ = int(self.M_Text.text())
                    rate = int(self.rateText.text())
                    func.run_sSMC_FCM()
                except:
                    self.error_dialog = QtWidgets.QErrorMessage()
                    self.error_dialog.showMessage('Please fill all input of sSMC-FCM!')
                    
                
if __name__ == '__main__':
    app = QApplication([])
    mainWindow = MyWindowClass()
    mainWindow.show()
    sys.exit(app.exec_())