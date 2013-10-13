'''
Created on Sep 10, 2013

@author: dinesh
'''

'''
     This class determines the correct type of command and
     returns the correct type to the caller.
     
'''
from CustomerOperations import AddCustomer
from ShopOperations import AddShop, ViewShops, RetrieveShop
from LocationOperations import AddLocation, ViewLocation
from StockOperations import AddStock
from ManufacturerOperations import AddManufacturer,ViewManufacturers
from CategoryOperations import AddCategory,ViewCategories
from ProductOperations import AddProduct, ViewProduct, SearchProductBarcode
from UserOperations import BuyItem

class CommandFactory(object):
    
    def createCommand(self,operation,formData):
        if operation == "addcustomer":
            addCustomerCommand = AddCustomer()
            return addCustomerCommand

        elif operation == "addshop":
        	addShopCommand = AddShop()
        	return addShopCommand

        elif operation == "retrieveshop":
            retriveShopCommand = RetrieveShop()
            return retriveShopCommand
        
        elif operation == "viewshops":
            viewShopCommand = ViewShops()
            return viewShopCommand

        elif operation == "addlocation":
        	addLocationCommand = AddLocation()
        	return addLocationCommand

        elif operation == "viewlocation":
            viewLocationCommand = ViewLocation()
            return viewLocationCommand
        
        elif operation == "addmanufacturer":
            addManufacturerCommand = AddManufacturer()
            return addManufacturerCommand

        elif operation == "addstock":
        	addStockCommand = AddStock()
        	return addStockCommand
  
        elif operation == "addcategory":
            addCategoryCommand = AddCategory()
            return addCategoryCommand
        
        elif operation == "addproduct":
            addProductCommand = AddProduct()
            return addProductCommand
        
        elif operation == "viewmanufacturers":
            viewManufacturersCommand = ViewManufacturers()
            return viewManufacturersCommand
        
        elif operation == "viewcategories":
            viewCategoriesCommand = ViewCategories()
            return viewCategoriesCommand

        elif operation == "viewproducts":
            viewProductCommand = ViewProduct()
            return viewProductCommand

        elif operation == "buyitem":
            buyItemCommand = BuyItem()
            return buyItemCommand
        
        elif operation == "searchBarcode":
            searchBarcodeCommand = SearchProductBarcode()
            return searchBarcodeCommand
     
