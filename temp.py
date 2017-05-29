class Base:
	def __init__(self):
		self.name = 'weiyanyu'

	def eat(self):
		print('doing')

	def do(self):
		print('doing')


class Dog(Base):
	def __init__(self,EngName):
		super().__init__()
		self.EngName = EngName

	def show(self):
		print(self.name)
		print(self.EngName)


d = Dog('YEONON')
d.show()