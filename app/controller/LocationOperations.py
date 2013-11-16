from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

class AddLocation(Command): 
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()

    def execute(self,formData):
        print "here addlocation"
        if self.__check_database(formData):

            self.storageObject.add_location_to_database(formData)
            self.feedbackObject.setinfo("Success: data added ")
            self.feedbackObject.setdata(formData.country.data)
            self.feedbackObject.setcommandtype("AddLocation")
        else:
            self.feedbackObject.setinfo("Faiure: data present already ")
            self.feedbackObject.setdata("data present")
            self.feedbackObject.setcommandtype("AddLocation")
        return self.feedbackObject

    def __check_database(self, formData):
        return self.storageObject.location_query_database(formData)

class ViewLocation(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()

    def execute(self, formData):
        return self.get_locations(formData)

    def get_locations(self, formData):
        return self.storageObject.get_all_location(formData)