import requests
import re
from bs4 import BeautifulSoup
import os
import csv
import sys 
from collections import defaultdict



class Zhilian_Info():
	def __init__(self):
		self.main_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s&kw=%s&sm=0&p=%s"
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36"
		self.headers = {
			'user-agent' : self.user_agent
		}
		self.job_infos = []
		self.file_path = os.path.abspath('..') + '/resource/zhilian/'

	#根据参数获得响应
	def request_url(self):
		for i in range(20):			#20 为可选参数
			r = requests.get(self.main_url % ("北京","石油 机械",i),headers=self.headers)  #参数可选
			soup = BeautifulSoup(r.text)
			yield soup

	#获得对应的职位列表
	def get_job_list(self):
		for soup in self.request_url():
			job_list = soup.find_all('table', class_='newlist')
			yield job_list
		

	#开始保存提取到的信息
	def get_job_info(self):
		soup = self.request_url()

		for job_list in self.get_job_list():
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
				self.job_infos.append(info)
		
		return self.job_infos

	#对工资划分区间，用于绘图，原始数据未改变
	def salary_handle(self):
		salarys = defaultdict(int)

		for job_info in self.job_infos:
			salary = job_info['salary']
			if salary >= 0 and salary < 5000:
				salarys['0-5000'] += 1
			elif salary >= 5000 and salary < 8000:
				salarys['5000-8000'] += 1
			elif salary >= 8000 and salary <= 12000:
				salarys['8000-12000'] += 1
			elif salary >= 12000 and salary <= 15000:
				salarys['12000-15000'] += 1
			else:
				salarys['15000-~'] += 1

		with open(self.file_path + 'salary_for_image.csv','w',encoding='utf-8') as f:
			f.write(str('salary') + '\n')
			for salary,num in salarys.items():
				f.write(str(salary) + ',')
				f.write(str(num) + '\n')

	#对位置分类并统计
	def position_handle(self):
		postions = defaultdict(int)

		for job_info in self.job_infos:
				postion = job_info['position'].split('-')
				if len(postion) == 2:
					postion = postion[1]
				else:
					postion = postion[0]
				postions[postion] += 1

		with open(self.file_path + 'postion_for_image.csv','w',encoding='utf-8') as f:
			f.write(str('postion') + '\n')
			for postion,num in postions.items():
				f.write(str(postion) + ',')
				f.write(str(num) + '\n')

	#保存文件
	def saveFile(self,fileName):
		with open(self.file_path + fileName + '.csv','w',encoding='utf-8') as f:
			f.write(str('position') + '\n')
			for job_info in self.job_infos:
				f.write(str(job_info[fileName]) + '\n')


if __name__ == '__main__':
	Info = Zhilian_Info()
	for info in Info.get_job_info():
		print(info)

	Info.saveFile('salary')
	Info.saveFile('position')
	Info.salary_handle()
	Info.position_handle()

