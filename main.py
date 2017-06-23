#导入python 语言自带库
import threading
import webbrowser
import gc
import sqlite3
import xlwt

#导入自写类
from mainWIndow import *
from zhilian.zhilian import ZhilianCrawl
from lagou.lagou import LagowCrwal
from GenImage import GenImage



class Main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.type = ""
        self.staff_list = []
        self.InitImage()
        self.showStaff()
        self.ItemNumber = 0

    def typeMap(self, type):
        if type == "拉勾网":
            return "lagou"
        elif type == "智联":
            return "zhilian"
        else:
            return "zhilian"
    
    #初始化图片展示到GUI上
    def InitImage(self):
        self.db = sqlite3.connect('jobs.db')
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM latestType")
        self.type = cursor.fetchall()[0][1]
        cursor.close()
        self.db.commit()

        PixMapSalary = QtGui.QPixmap(os.getcwd() + '/resource/%s/images/1.png' % self.type).scaled(400,600)
        self.SalaryImage.setPixmap(PixMapSalary)
        PixMapPosition = QtGui.QPixmap(os.getcwd() + '/resource/%s/images/2.png' % self.type).scaled(500,500)
        self.PositionImage.setPixmap(PixMapPosition)

    #开启主线程外的另一个线程，防止UI阻塞，注意到在那个线程里爬数据的时候再次开启了多线程，这是可以的，也是python和Qt 灵活的地方
    def work(self):
        position = self.positionEdit.text()
        position = position.strip()
        if position == '':
            position = '北京'                             #为避免数据错乱，如用户不输入地点，则默认为北京

        self.type = self.typeMap(self.TypeBox.currentText())    

        keyword = self.keywordEdit.text()
        page_number = self.spinBox.value()

        if self.type == 'lagou':
            self.workTheard = LagowCrwal(position, keyword, self.progressBar, page_number)
        elif self.type == 'zhilian':
            self.workTheard = ZhilianCrawl(position, keyword, self.progressBar, page_number)
        else:
            self.workTheard = ZhilianCrawl(position, keyword, self.progressBar, page_number)
        self.workTheard.start()
        self.workTheard.trigger.connect(self.showImage)
    
    def showStaff(self):
        cursor = self.db.cursor()
        self.staff_list = []
        self.listWidget.clear()                                 #staff_list 常驻内存，切记每次都要初始化为空，否则列表将无限增长，最终程序崩溃
        
        #从数据库中得到所有职位信息
        
        cursor.execute('SELECT * FROM %s' % (self.type))
        values = cursor.fetchall()
        N = 50 if len(values) >= 50 else len(values)

        for i in range(N):    
            self.staff_list.append(values[i][0] + ',' + values[i][3])
            staff = self.staff_list[i].split(',')[0]
            self.listWidget.addItem(staff)
        
        cursor.close()
        self.db.commit()

     
    #将图像显示到界面上来，使用QLabel
    def showImage(self): 
        #这里本来想在后台执行的，但是会造成 main thread is not in main loop 的错误，既然不在main loop中，我就直接把他放到主线程中来，虽然这样可能会短暂阻塞UI，但是用户基本感觉不到
        try:
            image = GenImage(os.getcwd() + '/resource/%s/' % (self.type))
            image.generateImage('position_for_image.csv','1.png','bar')				
            image.generateImage('salary_for_image.csv','2.png','pie')
        except:
            self.networkError()
        
        PixMapSalary = QtGui.QPixmap(os.getcwd() + '/resource/%s/images/1.png' % (self.type)).scaled(400,600)
        self.SalaryImage.setPixmap(PixMapSalary)
        PixMapPosition = QtGui.QPixmap(os.getcwd() + '/resource/%s/images/2.png' % (self.type)).scaled(500,500)
        self.PositionImage.setPixmap(PixMapPosition)

        del image
        gc.collect()
        #读取新的数据
        self.showStaff()

    #用于给用户双击职位名称即可通过浏览器看到详细的信息，使用webbrowser来实现
    def showItem(self):
        current_row = self.listWidget.currentRow()
        for i in range(current_row + 1):
            if i == current_row:
                url = self.staff_list[i].split(',')[1]
                webbrowser.open_new(url)


    def openFile(self):
        DirName = QtWidgets.QFileDialog.getExistingDirectory(self.Filedialog, "浏览文件",
                            "C:",QtWidgets.QFileDialog.ShowDirsOnly)
        self.DirlineEdit.setText(DirName)


    def saveFileToExcel(self):
        fileName = self.FilelineEdit.text()
        if fileName == '':
            fileName = 'default'

        fileName = self.DirlineEdit.text() + '/' + fileName
        
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM %s' % (self.type))
        values = cursor.fetchall()

        workBook = xlwt.Workbook(encoding='ascii')
        workSheet = workBook.add_sheet('职位信息')

        workSheet.write(0, 0, '职位')
        workSheet.write(0, 1, '薪水')
        workSheet.write(0, 2, '位置')
        for i in range(len(values)):
            workSheet.write(i+1, 0, values[i][0])
            workSheet.write(i+1, 1, values[i][1])
            workSheet.write(i+1, 2, values[i][2])

        workBook.save(fileName + '.xls')

        SucessMessage = QtWidgets.QMessageBox.information( self, 
                                                            '导出EXCEL',
                                                            '导出成功',
                                                            QtWidgets.QMessageBox.Yes)


    

    #网络异常的时候，弹出消息框，但不退出程序
    def networkError(self):
        self.NetworkErrorMessage = QtWidgets.QMessageBox.critical(  self,
                                                                    '网络错误',
                                                                    '请检查网络连接',
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