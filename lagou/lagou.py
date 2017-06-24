import requests,json
import sys
from collections import defaultdict
from queue import Queue
import threading
import os
from PyQt5.QtCore import *
import time
import re
import sqlite3


sys.path.append('../')
from CrawlBase import CrawlBase
from GenImage import GenImage



class LagowCrwal(CrawlBase):
	trigger = pyqtSignal()
	def __init__(self, position, keyword, progressBar, page_number):
		super().__init__()
		self.main_url = "http://www.lagou.com/jobs/positionAjax.json?px=default&city=%s&first=true&kd=%s&pn=%s"
		self.POSITION = position
		self.file_path = os.getcwd() + '/resource/lagou/'	
		self.job_infos = []
		self.KEYWORD = keyword
		self.page_number = page_number
		self.url_queue = self.generateUrl()
		self.MyLock = threading.Lock()

		self.progressBar = progressBar
		self.progressBarStep = 0
		self.page_number = page_number
		self.progressBarPerStep = 100 / self.page_number





	def generateUrl(self):
		q = Queue()
		for i in range(self.page_number):
			url = self.main_url % (self.POSITION, self.KEYWORD, i)
			q.put(url)

		return q

	def processUrl(self):
		while not self.url_queue.empty():
			url = self.url_queue.get()
			self.getRandomUserAgent()
			self.getRandomIP()
			try:
				time.sleep(1)															#用户有可能在断网的环境先执行，为避免因网络原因导致强退，要执行Exception Checkout
				self.crawl(url)
				
			except TimeoutError as e:
				continue


	def run(self):
		self.progressBar.setValue(0)
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
		self.saveAll('lagou',db)																		#保存文件，单独存放职位名称和对应的URL
					

		self.trigger.emit()


	def crawl(self, url):
		try:
			r = requests.get(url, headers=self.headers, proxies = self.proxies, timeout=10)
			job_data = json.loads(r.text)['content']['positionResult']['result']
		except:
			self.url_queue.put(url)
			raise TimeoutError('错误')

		self.MyLock.acquire()
		self.progressBarStep += self.progressBarPerStep
		self.progressBar.setValue(self.progressBarStep)
		for job in job_data:
			infos = {}
			infos['staff'] = job['positionName']

			salary = job['salary']
			infos['salary'] = re.sub(r'k|K','000',salary)
			
			position = str(job['district'])
			if position == '':
				infos['position'] = self.POSITION
			else:
				infos['position'] = position
			infos['details_url'] = "https://www.lagou.com/jobs/%s.html" % (job['positionId'])
			self.job_infos.append(infos)

		self.MyLock.release()	
		self.url_queue.task_done()





