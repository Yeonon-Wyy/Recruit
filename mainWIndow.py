from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget
import sys
import os
from zhilian.zhilian import Zhilian
import threading


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1280, 720)

        #set mainwindow to center of desktop
        qr = MainWindow.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        MainWindow.move(qr.topLeft())

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.positionEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.positionEdit.setGeometry(QtCore.QRect(20, 40, 300, 30))
        self.positionEdit.setObjectName("positionEdit")

        self.keywordEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.keywordEdit.setGeometry(QtCore.QRect(390, 40, 500, 30))
        self.keywordEdit.setObjectName("keywordEdit")

        self.serchBtn = QtWidgets.QPushButton(self.centralwidget)
        self.serchBtn.setGeometry(QtCore.QRect(970, 40, 300, 30))
        self.serchBtn.setObjectName("serchBtn")
        self.serchBtn.clicked.connect(self.work)

        self.SalaryImage = QtWidgets.QLabel(self.centralwidget)
        self.SalaryImage.setGeometry(QtCore.QRect(520, 80, 440, 600))
        self.SalaryImage.setAlignment(QtCore.Qt.AlignCenter)
        self.SalaryImage.setObjectName("SalaryImage")
        

        self.PositionImage = QtWidgets.QLabel(self.centralwidget)
        self.PositionImage.setGeometry(QtCore.QRect(20, 80, 500, 600))
        self.PositionImage.setAlignment(QtCore.Qt.AlignCenter)
        self.PositionImage.setObjectName("PositionImage")

        PixMapSalary = QtGui.QPixmap(os.getcwd() + '/resource/zhilian/images/1.png').scaled(400,600)
        self.SalaryImage.setPixmap(PixMapSalary)
        PixMapPosition = QtGui.QPixmap(os.getcwd() + '/resource/zhilian/images/2.png').scaled(500,500)
        self.PositionImage.setPixmap(PixMapPosition)

        
        
        self.PositionLabel = QtWidgets.QLabel(self.centralwidget)
        self.PositionLabel.setGeometry(QtCore.QRect(20, 5, 300, 30))
        self.PositionLabel.setObjectName("PositionLabel")

        self.KeywordLabel = QtWidgets.QLabel(self.centralwidget)
        self.KeywordLabel.setGeometry(QtCore.QRect(390, 0, 500, 30))
        self.KeywordLabel.setObjectName("KeywordLabel")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(970, 80, 300, 600))
        self.listWidget.setObjectName("listWidget")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(970, 10, 300, 20))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)

        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 28))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.StaffTheard = HandleStaff(self.listWidget)
        self.StaffTheard.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.serchBtn.setText(_translate("MainWindow", "search"))
        #self.SalaryImage.setText(_translate("MainWindow", "Salary Image"))
        #self.PositionImage.setText(_translate("MainWindow", "Position Image"))
        self.PositionLabel.setText(_translate("MainWindow", "position:"))
        self.KeywordLabel.setText(_translate("MainWindow", "Key word:"))

    def work(self):
        position = self.positionEdit.text()
        keyword = self.keywordEdit.text()

        self.workTheard = Zhilian(position,keyword,self.progressBar)
        self.workTheard.start()
     
        self.workTheard.trigger.connect(self.show_image)


    def show_staff(self):
        with open(os.getcwd() + '/resource/zhilian/staff.txt') as f:
            for i in range(20):
                staff = f.readline()
                self.listWidget.addItem(staff)
        
    def show_image(self,job_list):
        PixMapSalary = QtGui.QPixmap(os.getcwd() + '/resource/zhilian/images/1.png').scaled(400,600)
        self.SalaryImage.setPixmap(PixMapSalary)
        PixMapPosition = QtGui.QPixmap(os.getcwd() + '/resource/zhilian/images/2.png').scaled(500,500)
        self.PositionImage.setPixmap(PixMapPosition)

        self.listWidget.clear()

        self.show_staff()

class HandleStaff(QtCore.QThread):
    def __init__(self,listWidget):
        super().__init__()
        self.listWidget = listWidget

    def run(self):
        with open(os.getcwd() + '/resource/zhilian/staff.txt') as f:
            for i in range(20):
                staff = f.readline()
                self.listWidget.addItem(staff)

        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_()) 










