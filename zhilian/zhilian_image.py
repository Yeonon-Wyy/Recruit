import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib
import sys
sys.path.append('../')
from config import Config


class Zhilian_generate_image:
	def generate_bar(self,fileName):
		matplotlib.rcParams['figure.figsize'] = 10,10
		mydata = pd.read_csv(os.path.abspath('..') + '/resource/zhilian/salary_for_image.csv',encoding="gb18030")
		
		mydata.plot(kind='bar',subplots=True)
		plt.savefig('/home/yeonon/desktop/Recruit/resource/zhilian/images/' + fileName)

if __name__ == '__main__':
	Image = Zhilian_generate_image()
	Image.generate_bar('1.png')
	print(os.path.abspath('..'))