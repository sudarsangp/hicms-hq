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
            self.feedbackObject.setdata(formData.shopId.data)
            self.feedbackObject.setcommandtype("AddShop")

        return self.feedbackObject

    def __check_database(self, formData):
        return self.storageObject.shop_query_database(formData)

class ViewShops(Command):
    def __init__(self):
        self.storageObject = StorageClass()

    def execute(self, formData):
        return self.get_shops()

    def get_shops(self):
        return self.storageObject.get_shops_from_db()

class RetrieveShop(Command):
    def __init__(self):
        self.storageObject = StorageClass()

    def execute(self, formData):
        return self.get_shop_for_shopid(formData)

    def get_shop_for_shopid(self, formData):
        return self.storageObject.get_shop_shopid_from_db(formData.shopId.data)

class UpdateShop(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
        
    def execute(self, formData):
        print formData.shopId.data
        self.storageObject.set_shop_details(formData)
        self.feedbackObject.setinfo("Success: data updated ")
        self.feedbackObject.setdata(formData.shopId.data)
        self.feedbackObject.setcommandtype("Update Shop")
        return self.feedbackObject
        
        