import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib


class ZhilianGenImage:
	def __init__(self):
		self.FILE_PATH = os.path.abspath('.') + '/resource/zhilian/'
		self.FONT = {
			'size' : 20
		 }

	def generate_image(self,sourceName,fileName,image_kind):
		matplotlib.rcParams['font.family'] = 'SimHei'
		matplotlib.rc('font', **self.FONT)               
		mydata = pd.read_csv(self.FILE_PATH + sourceName)
		mydata.sort_index()

		if image_kind == 'pie':
			mydata.plot(kind='pie',subplots=True, figsize=(10,10),autopct='%1.1f%%',fontsize=15)
		elif image_kind == 'barh':
			mydata.plot(kind='barh',subplots=True,fontsize=20,figsize=(16,6))
		else:
			raise TypeError('参数错误')

		plt.savefig(self.FILE_PATH + 'images/' + fileName)
