from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

class PriceCalculator(Command):

	def __init__(self):
		self.storageObject = StorageClass()
		self.feedbackObject = Feedback()

	def execute(self,formData):
		list_bar_price = self.storageObject.all_barcode_acitve_price()
		#self.feedbackObject = feedback
		return list_bar_price

