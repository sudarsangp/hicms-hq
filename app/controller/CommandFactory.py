'''
Created on Sep 10, 2013

@author: dinesh
'''

'''
     This class determines the correct type of command and
     returns the correct type to the caller.
     
'''
from CustomerOperations import AddCustomer
from ShopOperations import AddShop
from LocationOperations import AddLocation

class CommandFactory(object):
    
    def createCommand(self,operation,formData):
        if operation == "addcustomer":
            addCustomerCommand = AddCustomer()
            return addCustomerCommand

        elif operation == "addshop":
        	addShopCommand = AddShop()
        	return addShopCommand

        elif operation == "addlocation":
        	addLocationCommand = AddLocation()
        	return addLocationCommand
        
        
    