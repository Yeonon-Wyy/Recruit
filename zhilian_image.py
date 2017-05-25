import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
	#mydata = pd.read_csv(os.getcwd() + '/resource/salary.csv')

	s = pd.Series(np.random.randn(10).cumsum(), index=np.arange(0, 100, 10))
	s.plot()

	#print(type(mydata))
	#print(mydata.index)