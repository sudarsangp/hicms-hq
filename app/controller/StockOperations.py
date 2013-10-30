
from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

class AddStock(Command):
    
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
         
    def execute(self,formData):

        if self.check_existing_item(formData):
            self.feedbackObject.setinfo("Failed :Duplicate Data present cannot be added")
            self.feedbackObject.setdata(formData.barcode.data)
            self.feedbackObject.setcommandtype("AddStock")
     
        else:
            self.storageObject.addStockToDatabase(formData)
            self.feedbackObject.setinfo("Success: data added ")
            self.feedbackObject.setdata(formData.barcode.data)
            self.feedbackObject.setcommandtype("AddStock")
     
        return self.feedbackObject

    def check_existing_item(self, formData):
        return self.storageObject.check_if_stock_exists(formData)

class ViewStock(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()

    def execute(self, formData):
        return self.get_stock()

    def get_stock(self):
        return self.storageObject.get_stock_from_db()

class SearchStockByShopId(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()

    def execute(self, formData):
        return self.get_stock_for_shopId(formData)

    def get_stock_for_shopId(self, formData):
        return self.storageObject.get_stock_grouped_shopId(formData.shopId.data)

class UpdateStock(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()

    def execute(self, formData):
        if self.storageObject.check_if_stock_exists(formData):
            #print formData.barcode.data
            self.storageObject.update_stock(formData)
            self.feedbackObject.setinfo("Success: data updated ")
            self.feedbackObject.setdata(formData.barcode.data)
            self.feedbackObject.setcommandtype("UpdateStock")
            
        else:
            self.feedbackObject.setinfo("Failed :Duplicate Data present cannot be added")
            self.feedbackObject.setdata(formData.barcode.data)
            self.feedbackObject.setcommandtype("UpdateStock")
     
        return self.feedbackObject