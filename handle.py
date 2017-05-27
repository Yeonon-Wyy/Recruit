from zhilian.zhilian_image import ZhilianGenImage
from zhilian.zhilian import Zhilian

from PyQt5.QtCore import *


class Handle(QThread):
	trigger = pyqtSignal(list)
	def __init__(self,postion,keyword):
		super(Handle,self).__init__()
		self.postion = postion
		self.keyword = keyword

	def run(self):
		zhilian_info = Zhilian(self.postion,self.keyword)
		zhilian_image = ZhilianGenImage()
		print('en')

		job_list = zhilian_info.get_job_info()


		zhilian_image.generate_image('postion_for_image.csv','1.png','bar')
		zhilian_image.generate_image('salary_for_image.csv','2.png','pie')

		self.trigger.emit(job_list)





