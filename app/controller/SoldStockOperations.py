from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

class AddSoldStock(Command):
    
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
         
    def execute(self,formData):

        #if self.check_existing_item(formData):
        
        self.storageObject.add_sold_stock_to_database(formData)
        self.feedbackObject.setinfo("Success: data added ")
        self.feedbackObject.setdata(formData.barcode.data)
        self.feedbackObject.setcommandtype("AddSoldStock")
        #else:
        #    self.feedbackObject.setinfo("Failed :Duplicate Data present cannot be added")
        #    self.feedbackObject.setdata(formData.barcode.data)
        #    self.feedbackObject.setcommandtype("AddSoldStock")
     
        return self.feedbackObject

    def check_existing_item(self, formData):
        return self.storageObject.check_if_sold_stock_exists(formData) 

class ViewSoldStock(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()

    def execute(self, formData):
        return self.get_soldstock()

    def get_soldstock(self):
        return self.storageObject.get_soldstock_from_db()

class SearchSoldStockByShopId(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()

    def execute(self, formData):
        return self.get_transactions_for_shopId(formData)

    def get_transactions_for_shopId(self, formData):
        return self.storageObject.get_transaction_grouped_shopId(formData.shopId.data)