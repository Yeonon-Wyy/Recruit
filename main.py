from mainWIndow import *


class Main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

    #start anothor thread in order to execu crawl job infomation and avoid UI is blocked
    def work(self):
        position = self.positionEdit.text()
        keyword = self.keywordEdit.text()
        page_number = self.spinBox.value()

        self.workTheard = Zhilian(position,keyword,self.progressBar,page_number)
        self.workTheard.start()

        
        self.workTheard.trigger2.connect(self.networkError)
        self.workTheard.trigger.connect(self.show_image)





    #slot function
    
    def show_staff(self):
        print('show')
        self.StaffTheard = HandleStaff(self.listWidget)
        self.StaffTheard.start()
      

    def show_image(self,job_list):
        PixMapSalary = QtGui.QPixmap(os.getcwd() + '/resource/zhilian/images/1.png').scaled(400,600)
        self.SalaryImage.setPixmap(PixMapSalary)
        PixMapPosition = QtGui.QPixmap(os.getcwd() + '/resource/zhilian/images/2.png').scaled(500,500)
        self.PositionImage.setPixmap(PixMapPosition)

        self.listWidget.clear()
        self.show_staff()
    
        


    def show_item(self):
        print(self.listWidget.currentItem().text())
        print(self.listWidget.currentRow())
        current_row = self.listWidget.currentRow()
        with open(os.getcwd() + '/resource/zhilian/staff.txt','r') as f:
            for i in range(current_row + 1):
                line = f.readline()
                if i == current_row:
                    url = line.split(',')[1]
                    print(url)
                    webbrowser.open(url)
                    break


        #webbrowser.open('http://www.baidu.com')




    def networkError(self):
        self.NetworkErrorMessage = QtWidgets.QMessageBox.critical(  self,
                                                                    'network',
                                                                    'please checkout the network connection',
                                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        try:
            self.NetworkErrorMessage.show()
        except:
            pass




        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Main()
    MainWindow.show()
    sys.exit(app.exec_()) 