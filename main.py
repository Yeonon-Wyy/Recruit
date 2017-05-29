from mainWIndow import *


class Main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.staff_list = []

    

    #开启主线程外的另一个线程，防止UI阻塞，注意到在那个线程里爬数据的时候再次开启了多线程，这是可以的，也是python和Qt 灵活的地方
    def work(self):
        position = self.positionEdit.text()
        position = position.strip()
        if position == '':
            position = '北京'                             #为避免数据错乱，如用户不输入地点，则默认为北京

    
        keyword = self.keywordEdit.text()
        page_number = self.spinBox.value()

        self.workTheard = Zhilian(position,keyword,self.progressBar,page_number)
        self.workTheard.start()
     
        self.workTheard.trigger2.connect(self.networkError)
        self.workTheard.trigger.connect(self.show_image)



    #槽函数    
    def save_staff(self,staff_list):
        self.staff_list = staff_list

    #将图像显示到界面上来，使用QLabel
    def show_image(self):
        PixMapSalary = QtGui.QPixmap(os.getcwd() + '/resource/zhilian/images/1.png').scaled(400,600)
        self.SalaryImage.setPixmap(PixMapSalary)
        PixMapPosition = QtGui.QPixmap(os.getcwd() + '/resource/zhilian/images/2.png').scaled(500,500)
        self.PositionImage.setPixmap(PixMapPosition)

        self.listWidget.clear()
        
        #读取新的数据
        self.StaffTheard = HandleStaff(self.listWidget)
        self.StaffTheard.start()
        self.StaffTheard.trigger.connect(self.save_staff)
    
        

    #用于给用户双击职位名称即可通过浏览器看到详细的信息，使用webbrowser来实现
    def show_item(self):
        print(self.listWidget.currentItem().text())
        print(self.listWidget.currentRow())
        current_row = self.listWidget.currentRow()

        for i in range(current_row + 1):
            if i == current_row:
                url = self.staff_list[i].split(',')[1]
                print(url)
                webbrowser.open_new(url)
        """
        with open(os.getcwd() + '/resource/zhilian/staff.txt','r') as f:
            for i in range(current_row + 1):
                line = f.readline()
                if i == current_row:
                    url = line.split(',')[1]
                    print(url)
                    webbrowser.open(url)
                    break
        """


    #网络异常的时候，弹出消息框，但不退出程序
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