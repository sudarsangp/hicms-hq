from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

class AddShop(Command):

    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()

    def execute(self,formData):

        if self.__check_database(formData):

            self.storageObject.addShopTODatabase(formData)
            self.feedbackObject.setinfo("Success: data added ")
            self.feedbackObject.setdata(formData)
            self.feedbackObject.setcommandtype("AddCustomer")

        return self.feedbackObject

    def __check_database(self, formData):
        return self.storageObject.shop_query_database(formData)
    
