
class Feedback(object):

	def __init__(self,commandtype, info, data):
		self.commandtype = commandtype
		self.info = info
		self.data = data

	def setinfo(self, info):
		self.info = info

	def getinfo(self):
		return self.info

	def setdata(self, data):
		self.data = data

	def getdata(self):
		return self.data

	def setcommandtype(self, commandtype):
		self.commandtype = commandtype

	def getcommandtype(self):
		return self.commandtype

	def checkinfo(self, info):
		if self.info == info :
			return True
		else:
			return False