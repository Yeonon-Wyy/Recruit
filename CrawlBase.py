from collections import defaultdict
import random,re
from PyQt5.QtCore import QThread
import requests
from bs4 import BeautifulSoup


class CrawlBase(QThread):
	def __init__(self):
		super().__init__()
		self.user_agents=['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \(KHTML, like Gecko) Element Browser 5.0',
                   'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
                   'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                   'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                   'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \Version/6.0 Mobile/10A5355d Safari/8536.25',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/28.0.1468.0 Safari/537.36',
                   'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)'
                   ]
		self.IPList = [
			{'http': '115.220.6.209:808', 'https': '115.220.6.209:808'},
			{'http': '114.218.2.209:808', 'https': '114.218.2.209:808'},
			{'http': '139.224.237.33:8888', 'https': '139.224.237.33:8888'},
			{'http': '116.226.90.12:808', 'https': '116.226.90.12:808'},
			{'http': '218.108.107.70:909', 'https': '218.108.107.70:909'},
			{'http': '112.111.4.210:8118', 'https': '112.111.4.210:8118'},
			{'http': '140.250.78.132:808', 'https': '140.250.78.132:808'},
			{'http': '223.156.250.97:80', 'https': '223.156.250.97:80'},
			{'http': '125.118.69.94:808', 'https': '125.118.69.94:808'},
			{'http': '113.250.180.64:8118', 'https': '113.250.180.64:8118'},

		]
		self.headers = {}
		self.proxies = {}
		self.job_infos = []													#保存信息到内存中（暂时）

	#生成url 队列
	def generateUrl(self):
		pass

	def processUrl(self):													#作为多线程的目标函数
		pass

	def crawl(self,url):
		pass

	#随机从列选择使用
	def getRandomUserAgent(self):
		index = random.randint(0,len(self.user_agents) - 1)
		self.headers = {
			'user-agent' : self.user_agents[index]
		}

	#随机从列表选取使用
	def getRandomIP(self):
		index = random.randint(0,len(self.IPList) - 1)
		self.proxies = self.IPList[index]

	#获取代理IP
	def getListProxies(self):  
		session = requests.session()
		self.getRandomUserAgent()  
		page = session.get("http://www.xicidaili.com/nn", headers=self.headers)  
		soup = BeautifulSoup(page.text, 'lxml')  

		proxyList = []  
		taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})  
		for trtag in taglist:  
		    tdlist = trtag.find_all('td')  
		    proxy = {'http': tdlist[1].string + ':' + tdlist[2].string,  
		             'https': tdlist[1].string + ':' + tdlist[2].string}  
		    url = "http://ip.chinaz.com/getip.aspx"  #用来测试IP是否可用的url  
		    try:  
		        response = session.get(url, proxies=proxy, timeout=2)  
		        proxyList.append(proxy)  
		        if(len(proxyList) == 10):  
		            break  
		    except Exception as e:  
		        continue  

		return proxyList
	
	#对工资划分区间，用于绘图，原始数据未改变
	def salaryHandle(self):
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

		with open(self.file_path + fileName, 'w', encoding='utf-8') as f:
			f.write(str('薪水') + '\n')
			for salary, num in salarys.items():
				f.write(str(salary) + ',')
				f.write(str(num) + '\n')


	#对位置分类并统计
	def positionHandle(self):
		fileName = 'position_for_image.csv'
		positions = defaultdict(int)

		for job_info in self.job_infos:
				position = job_info['position'].split('-')
				if len(position) == 2:
					position = position[1]
				else:
					position = position[0]
				positions[position] += 1

		with open(self.file_path + fileName, 'w', encoding='utf-8') as f:
			f.write(str('位置') + '\n')
			for position, num in positions.items():
				f.write(str(position) + ',')
				f.write(str(num) + '\n')


	def staffHandle(self):
		fileName = 'staff.txt'
		with open(self.file_path + fileName, 'w', encoding='utf-8') as f:
			for job_info in self.job_infos:
				f.write(str(job_info['staff']) + ',' + str(job_info['details_url'] + '\n'))


	#保存文件，用户可提取
	def saveFileCSV(self, fileName):
		with open(self.file_path + fileName + '.csv', 'w', encoding='utf-8') as f:
			f.write(str(fileName) + '\n')
			for job_info in self.job_infos:
				f.write(str(job_info[fileName]) + '\n')

	#保存所有信息，用户可提取
	def saveAll(self):
		with open(self.file_path + 'AllInfo.txt', 'w', encoding='utf-8') as f:
			for job_info in self.job_infos:
				f.write(str(job_info) + '\n')

