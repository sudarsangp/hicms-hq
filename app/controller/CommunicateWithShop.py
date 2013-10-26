from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

import requests, json

url = 'http://localhost:8000/shopserverinfo'
fname = 'newitems.txt'

class UpdateShopServer(Command):
	def __init__(self):
		self.storageObject = StorageClass()
		self.feedbackObject = Feedback()

	def execute(self, formData):
		send_json = {}
		try:
		   with open(fname):
				f = open(fname,"r")
				contentdata = f.read()
				list_content = contentdata.split(';')
				send_json = {'update': list_content}
				final_json = json.dumps(send_json)
				r = requests.post(url,data=final_json)
				self.feedbackObject.setinfo("Success: data sent to shop server")
				self.feedbackObject.setdata(r.json())
				self.feedbackObject.setcommandtype("UpdateShopServer")
				return self.feedbackObject
		except IOError:
			self.feedbackObject.setinfo("File Does Not Exist")
			self.feedbackObject.setdata("No data")
			self.feedbackObject.setcommandtype("UpdateShopServer")
			return self.feedbackObject
