from collections import defaultdict

from PyQt5.QtCore import QThread

class CrawlBase(QThread):
	def __init__(self):
		super().__init__()
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36"
		self.headers = {
			'user-agent' : self.user_agent
		}
		self.job_infos = []													#保存信息到内存中（暂时）

	#生成url 队列
	def generate_url(self):
		pass

	def process_url(self):													#作为多线程的目标函数
		while not self.url_queue.empty():
			url = self.url_queue.get()
			try:															#用户有可能在断网的环境先执行，为避免因网络原因导致强退，要执行Exception Checkout
				self.crawl(url)
			except TimeoutError as e:
				print('继续')
				continue

	def crawl(self,url):
		pass

	
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

