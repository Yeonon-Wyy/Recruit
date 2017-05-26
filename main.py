from zhilian.zhilian import Zhilian
from zhilian.zhilian_image import ZhilianGenImage


if __name__ == '__main__':
	zhilian_info = Zhilian()
	zhilian_image = ZhilianGenImage()

	zhilian_info.get_job_info()
	salary_fileName = zhilian_info.salary_handle()
	postion_fileName = zhilian_info.position_handle()

	zhilian_image.generate_image(salary_fileName,'1.png','pie')
	zhilian_image.generate_image(postion_fileName,'2.png','pie')

