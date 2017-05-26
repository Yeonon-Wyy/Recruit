from zhilian.zhilian import Zhilian_Info
from zhilian.zhilian_image import Zhilian_generate_image


if __name__ == '__main__':
	zhilian_info = Zhilian_Info()
	zhilian_image = Zhilian_generate_image()

	zhilian_info.get_job_info()
	salary_fileName = zhilian_info.salary_handle()
	postion_fileName = zhilian_info.position_handle()

	print(salary_fileName)

	zhilian_image.generate_image(salary_fileName,'1.png','pie')
	zhilian_image.generate_image(postion_fileName,'2.png','pie')

