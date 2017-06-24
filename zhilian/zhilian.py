#导入python库
import requests
from bs4 import BeautifulSoup
import os
import csv
import sys
from collections import defaultdict
from queue import Queue
import threading
import time
from PyQt5.QtCore import *
import sqlite3

#导入自写类
sys.path.append('../')
from CrawlBase import CrawlBase 
from GenImage import GenImage



class ZhilianCrawl(CrawlBase):
	trigger = pyqtSignal()
	def __init__(self,position,keyword,progressBar,page_number):
		super().__init__()
		self.main_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s&kw=%s&sm=0&p=%s"
		self.job_infos = []																		#保存信息到内存中（暂时）
		self.file_path = os.getcwd() + '/resource/zhilian/'										#通用路径
		self.POSITION = position					
		self.KEYWORD = keyword
		self.progressBar = progressBar
		self.progressBarStep = 0
		self.page_number = page_number
		self.progressBarPerStep = 100 / self.page_number
		self.url_queue = self.generateUrl()													#url队列，用于多线程
		self.MyLock = threading.Lock()															#线程锁，保证线程同步


	#以下是继承自基类的方法，根据不同的情况（网站） 重写，实现多态

	#生成url 队列
	def generateUrl(self):
		q = Queue()
		for i in range(self.page_number):
			url = self.main_url % (self.POSITION,self.KEYWORD,i)								#直接通过参数生成队列
			q.put(url)
		return q

	def processUrl(self):
		while not self.url_queue.empty():
			url = self.url_queue.get()
			try:															#用户有可能在断网的环境先执行，为避免因网络原因导致强退，要执行Exception Checkout
				self.crawl(url)
			except TimeoutError as e:
				continue
	
	def run(self):
		self.progressBar.setValue(0)
		#这里的线程感觉存在问题，但是并不知道问题出现在哪（暂时这样吧，回去看看书）
		#开启多线程	这里暂定为4个线程（其实8个更好，为避免爬取速度过快，导致用户IP被封，故暂定4个
		t1 = threading.Thread(target=self.processUrl)
		t2 = threading.Thread(target=self.processUrl)
		t3 = threading.Thread(target=self.processUrl)
		t4 = threading.Thread(target=self.processUrl)
		t1.start()
		t2.start()
		t3.start()
		t4.start()
		t1.join()
		t2.join()
		t3.join()
		t4.join()
		
		db = self.InitDB()
		self.salaryHandle()																	#保存文件，单独存放薪水，用于方便生成图像，下同
		self.positionHandle()
		self.saveAll('zhilian',db)																		#保存文件，单独存放职位名称和对应的URL
					
		self.trigger.emit()																		#爬取完毕，要发送信号给UI主线程，并执行相应的槽函数

	
	def crawl(self,url):
		try:
			self.getRandomUserAgent()
			r = requests.get(url,headers=self.headers,timeout=10)
		except:
			raise TimeoutError('超时')
		soup = BeautifulSoup(r.text,'lxml')
		job_list = soup.find_all('table', class_='newlist')
		self.MyLock.acquire()																	#给进程上锁，保证同步，因为这里要修改共享的数据，self.job_infos
		self.progressBarStep += self.progressBarPerStep
		self.progressBar.setValue(self.progressBarStep)

		for job in job_list[1:]:
			info = {}
			info['staff'] = job.find_all('a')[0].text

			#处理工资
			info['salary'] = job.find('td',class_='zwyx').text
			
			#处理位置
			info['position'] = job.find('td',class_='gzdd').text


			info['details_url'] = job.find_all('a')[0].get('href')

			self.job_infos.append(info)														#修改共享数据
		self.MyLock.release()	
		self.url_queue.task_done()																#务必要解锁，否则其他线程永远无法进入这个部分，但是其他线程又已经从URL队列里得到url并请求了，最终会导致爬取数据不全

	

