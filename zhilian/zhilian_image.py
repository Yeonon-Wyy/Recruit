import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib


class Zhilian_generate_image:
	def __init__(self):
		self.FILE_PATH = os.path.abspath('..') + '/resource/zhilian/'
		self.FONT = {
			'family' : 'normal',
			'size' : 20
		 }

	def generate_image(self,sourceName,fileName,image_kind):
		matplotlib.rc('font', **self.FONT)               
		mydata = pd.read_csv(self.FILE_PATH + sourceName)
		mydata.sort_index()

		if image_kind == 'pie':
			mydata.plot(kind='pie',subplots=True, figsize=(10,10),autopct='%1.1f%%',fontsize=20)
		elif image_kind == 'barh':
			mydata.plot(kind='barh',subplots=True,fontsize=20,figsize=(16,6))
		else:
			raise TypeError('参数错误')

		plt.savefig(os.path.abspath('..') + '/resource/zhilian/images/' + fileName)

if __name__ == '__main__':
	Image = Zhilian_generate_image()
	Image.generate_image('salary_for_image.csv','1.png','pie')
	Image.generate_image('salary_for_image.csv','2.png','barh')
	print(os.path.abspath('..'))