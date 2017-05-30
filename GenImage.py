"""
这个类使用Matplotlib 和 pandas 读取CSV文件生成简单的图像用于简单的分析,是个通用类
"""
import gc
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib




class GenImage:
	def __init__(self,filePath):
		self.FILE_PATH = filePath
		self.FONT = {
			'size' : 20
		}

	def generate_image(self,sourceName,fileName,image_kind):
		print('生成')
		matplotlib.rcParams['font.family'] = 'SimHei'			#设置中文支持（linux下有问题）
		matplotlib.rc('font', **self.FONT)               
		mydata = pd.read_csv(self.FILE_PATH + sourceName)		
		mydata.sort_index()

		if image_kind == 'pie':
			mydata.plot(kind='pie',subplots=True, figsize=(10,10),autopct='%1.1f%%',fontsize=20)
		elif image_kind == 'bar':
			mydata.plot(kind='bar',subplots=True,fontsize=10,figsize=(4,6))
		else:
			raise TypeError('参数错误')

		plt.savefig(self.FILE_PATH + 'images/' + fileName,dpi=100)
		plt.close()
	
