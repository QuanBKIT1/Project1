
class fillData:
    def __init__(self, app):
        self.app = app

    def fill_iris(self):
        self.app.dataPath.setText("C:/Users/Quan/iris.data")
        self.app.colLabelText.setText("5")
        self.app.colRText.setText("")
        self.app.numberClusterText.setText('3')
        self.app.epsilonText.setText('0.00001')
        self.app.maxIterText.setText('300')
        self.app.mText.setText('2')
        self.app.mLText.setText('1.1')
        self.app.mUText.setText('9.1')
        self.app.alphaText.setText('0.7')
        self.app.MText.setText('2')
        self.app.M1Text.setText('4')
        self.app.alphaText2.setText('0.6')
        self.app.rateText.setText('20')

    def fill_ecoli(self):
        self.app.dataPath.setText("C:/Users/Quan/ecoli.data")
        self.app.colLabelText.setText("9")
        self.app.colRText.setText("1")
        self.app.numberClusterText.setText('8')
        self.app.epsilonText.setText('0.00001')
        self.app.maxIterText.setText('300')
        self.app.mText.setText('2')
        self.app.mLText.setText('5.5')
        self.app.mUText.setText('6.5')
        self.app.alphaText.setText('')
        self.app.MText.setText('')
        self.app.M1Text.setText('')
        self.app.alphaText2.setText('')
        self.app.rateText.setText('')

    def fill_wdbc(self):
        self.app.dataPath.setText("C:/Users/Quan/wdbc.data")
        self.app.colLabelText.setText("2")
        self.app.colRText.setText("1")
        self.app.numberClusterText.setText('2')
        self.app.epsilonText.setText('0.00001')
        self.app.maxIterText.setText('300')
        self.app.mText.setText('2')
        self.app.mLText.setText('3.1')
        self.app.mUText.setText('9.1')
        self.app.alphaText.setText('')
        self.app.MText.setText('')
        self.app.M1Text.setText('')
        self.app.alphaText2.setText('')
        self.app.rateText.setText('')


    def fill_wine(self):
        self.app.dataPath.setText("C:/Users/Quan/wine.data")
        self.app.colLabelText.setText("1")
        self.app.colRText.setText("")
        self.app.numberClusterText.setText('3')
        self.app.epsilonText.setText('0.00001')
        self.app.maxIterText.setText('300')
        self.app.mText.setText('2')
        self.app.mLText.setText('1.1')
        self.app.mUText.setText('6.1')
        self.app.alphaText.setText('0.7')
        self.app.MText.setText('2')
        self.app.M1Text.setText('6')
        self.app.alphaText2.setText('0.6')
        self.app.rateText.setText('20')

