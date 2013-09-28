from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

class AddLocation(Command): 
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback(None, None, None)

    def execute(self,formData):

        if self.__check_database(formData):

            self.storageObject.add_location_to_database(formData)
            self.feedbackObject.setinfo("Success: data added ")
            self.feedbackObject.setdata(formData)
            self.feedbackObject.setcommandtype("AddLocation")

        return self.feedbackObject

    def __check_database(self, formData):
        return self.storageObject.location_query_database(formData)

class ViewLocation(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback(None, None, None)

    def execute(self, formData):
        return self.get_locations(formData)

    def get_locations(self, formData):
        return self.storageObject.get_all_location(formData)