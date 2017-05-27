from zhilian.zhilian_image import ZhilianGenImage
from zhilian.zhilian import Zhilian

from PyQt5.QtCore import *


class Handle(QThread):
	trigger = pyqtSignal()
	def __init__(self):
		super(Handle,self).__init__()

	def run(self):
		zhilian_info = Zhilian('北京','石油')
		zhilian_image = ZhilianGenImage()

		zhilian_info.get_job_info()
		salary_fileName = zhilian_info.salary_handle()
		postion_fileName = zhilian_info.position_handle()

		zhilian_image.generate_image('postion_for_image.csv','1.png','bar')
		zhilian_image.generate_image('salary_for_image.csv','2.png','pie')

		self.trigger.emit()





