import requests
from bs4 import BeautifulSoup
import os
import csv
import sys 
from collections import defaultdict
from . zhilian_image import ZhilianGenImage
from queue import Queue
import threading
import time



from PyQt5.QtCore import *



class Zhilian(QThread):
	trigger = pyqtSignal()
	trigger2 = pyqtSignal()
	def __init__(self,position,keyword,progressBar,page_number):
		super().__init__()
		self.main_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s&kw=%s&sm=0&p=%s"
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36"
		self.headers = {
			'user-agent' : self.user_agent
		}

		self.job_infos = []													#保存信息到内存中（暂时）
		self.file_path = os.path.abspath('.') + '/resource/zhilian/'		#通用路径
		self.POSITION = position					
		self.KEYWORD = keyword
		self.progressBar = progressBar
		self.progressBarStep = 0
		self.progressBarPerStep = 100 / page_number
		self.page_number = page_number

		self.url_queue = self.generate_url()								#url队列，用于多线程
		self.MyLock = threading.Lock()										#线程锁，保证线程同步

	#生成url 队列
	def generate_url(self):
		q = Queue()
		for i in range(self.page_number):
			url = self.main_url % (self.POSITION,self.KEYWORD,i)			#直接通过参数生成队列
			q.put(url)
		return q

	def process_url(self):													#作为多线程的目标函数
		while not self.url_queue.empty():
			url = self.url_queue.get()
			try:															#用户有可能在断网的环境先执行，为避免因网络原因导致强退，要执行Exception Checkout
				self.crawl(url)
			except TimeoutError as e:
				print('继续')
				continue
		
	def run(self):
		self.progressBar.setValue(0)
		#开启多线程	这里暂定为4个线程（其实8个更好，为避免爬取速度过快，导致用户IP被封，故暂定8个）
		t1 = threading.Thread(target=self.process_url)
		t2 = threading.Thread(target=self.process_url)
		t3 = threading.Thread(target=self.process_url)
		t4 = threading.Thread(target=self.process_url)
		t1.start()
		t2.start()
		t3.start()
		t4.start()
		t1.join()
		t2.join()
		t3.join()
		t4.join()


		self.salary_handle()								#保存文件，单独存放薪水，用于方便生成图像，下同
		self.position_handle()
		self.saveAll()
		self.staff_handle()									#保存文件，单独存放职位名称和对应的URL

		zhilian_image = ZhilianGenImage()
		try:
			zhilian_image.generate_image('position_for_image.csv','1.png','bar')		#生成图像，同样，要Exception Checkout
			zhilian_image.generate_image('salary_for_image.csv','2.png','pie')
		except:
			self.trigger2.emit()

				

		self.trigger.emit()											#爬取完毕，要发送信号给UI主线程，并执行相应的槽函数

	def crawl(self,url):
		try:
			r = requests.get(url,headers=self.headers,timeout=10)
		except:
			raise TimeoutError('超时')
		soup = BeautifulSoup(r.text,'lxml')
		job_list = soup.find_all('table', class_='newlist')
		print(threading.current_thread())
		self.MyLock.acquire()								#给进程上锁，保证同步，因为这里要修改共享的数据，self.job_infos

		self.progressBarStep += self.progressBarPerStep
		self.progressBar.setValue(self.progressBarStep)

		for job in job_list[1:]:
			info = {}
			info['staff'] = job.find_all('a')[0].text

			#处理工资
			salary = job.find('td',class_='zwyx').text.split('-')
			if len(salary) == 2:
				info['salary'] = (int(salary[0]) + int(salary[1])) / 2
			else:
				info['salary'] = -1
			#处理位置
			info['position'] = job.find('td',class_='gzdd').text


			info['details_url'] = job.find_all('a')[0].get('href')

			self.job_infos.append(info)		#修改共享数据
		print('start_process')
		self.MyLock.release()								#务必要解锁，否则其他线程永远无法进入这个部分，但是其他线程又已经从URL队列里得到url并请求了，最终会导致爬取数据不全

	
	#对工资划分区间，用于绘图，原始数据未改变
	def salary_handle(self):
		fileName = 'salary_for_image.csv'
		salarys = defaultdict(int)
		#便于绘图，划分区间
		for job_info in self.job_infos:
			salary = job_info['salary']
			if salary >= 0 and salary < 5000:
				salarys['0-5K'] += 1
			elif salary >= 5000 and salary < 8000:
				salarys['5K-8K'] += 1
			elif salary >= 8000 and salary <= 12000:
				salarys['8K-12K'] += 1
			elif salary >= 12000 and salary <= 15000:
				salarys['12K-15K'] += 1
			else:
				salarys['15K-~'] += 1

		with open(self.file_path + fileName,'w',encoding='utf-8') as f:
			f.write(str('薪水') + '\n')
			for salary,num in salarys.items():
				f.write(str(salary) + ',')
				f.write(str(num) + '\n')

		return fileName

	#对位置分类并统计
	def position_handle(self):
		fileName = 'position_for_image.csv'
		positions = defaultdict(int)

		for job_info in self.job_infos:
				position = job_info['position'].split('-')
				if len(position) == 2:
					position = position[1]
				else:
					position = position[0]
				positions[position] += 1

		with open(self.file_path + fileName,'w',encoding='utf-8') as f:
			f.write(str('位置') + '\n')
			for position,num in positions.items():
				f.write(str(position) + ',')
				f.write(str(num) + '\n')

		return fileName

	def staff_handle(self):
		fileName = 'staff.txt'
		with open(self.file_path + fileName,'w',encoding='utf-8') as f:
			for job_info in self.job_infos:
				f.write(str(job_info['staff']) + ',' + str(job_info['details_url'] + '\n'))


	#保存文件，用户可提取
	def saveFile_csv(self,fileName):
		with open(self.file_path + fileName + '.csv','w',encoding='utf-8') as f:
			f.write(str(fileName) + '\n')
			for job_info in self.job_infos:
				f.write(str(job_info[fileName]) + '\n')

	#保存所有信息，用户可提取
	def saveAll(self):
		with open(self.file_path + 'AllInfo.txt','w',encoding='utf-8') as f:
			for job_info in self.job_infos:
				f.write(str(job_info) + '\n')

