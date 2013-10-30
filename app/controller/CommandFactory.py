'''
Created on Sep 10, 2013

@author: dinesh
'''

'''
     This class determines the correct type of command and
     returns the correct type to the caller.
     
'''
from CustomerOperations import AddCustomer
from ShopOperations import AddShop, ViewShops, RetrieveShop, UpdateShop, DeleteShop
from LocationOperations import AddLocation, ViewLocation
from StockOperations import AddStock, ViewStock, SearchStockByShopId
from ManufacturerOperations import AddManufacturer,ViewManufacturers
from CategoryOperations import AddCategory,ViewCategories
from ProductOperations import AddProduct, ViewProduct, SearchProductBarcode, RetrieveProduct, UpdateProduct, DeleteProduct, HQCacheStock
from UserOperations import BuyItem
from SoldStockOperations import AddSoldStock, ViewSoldStock, SearchSoldStockByShopId
from PriceCalculator import PriceCalculator

class CommandFactory(object):
    
    def createCommand(self,operation,formData):
        if operation == "addcustomer":
            addCustomerCommand = AddCustomer()
            return addCustomerCommand

        elif operation == "addshop":
        	addShopCommand = AddShop()
        	return addShopCommand

        elif operation == "retrieveshop":
            retrieveShopCommand = RetrieveShop()
            return retrieveShopCommand

        elif operation == "updateshop":
            updateShopCommand = UpdateShop()
            return updateShopCommand

        elif operation == "deleteshop":
            deleteShopCommand = DeleteShop()
            return deleteShopCommand

        elif operation == "viewshops":
            viewShopCommand = ViewShops()
            return viewShopCommand

        elif operation == "addproduct":
            addProductCommand = AddProduct()
            return addProductCommand

        elif operation == "retrieveproduct":
            retrieveProductCommand = RetrieveProduct()
            return retrieveProductCommand

        elif operation == "updateproduct":
            updateProductCommand = UpdateProduct()
            return updateProductCommand

        elif operation == "deleteproduct":
            deleteProductCommand = DeleteProduct()
            return deleteProductCommand
        
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

        elif operation == "addsoldstock":
            addSoldStockCommand = AddSoldStock()
            return addSoldStockCommand

        elif operation == "viewtransactions":
            viewTransactionCommand = ViewSoldStock()
            return viewTransactionCommand

        elif operation == "transactiongroupedbyshop":
            transactionByShopCommand = SearchSoldStockByShopId()
            return transactionByShopCommand
     
        elif operation == "cachestockqty":
            productStockCommand = HQCacheStock()
            return productStockCommand

        elif operation == "viewstock":
            viewStockCommand = ViewStock()
            return viewStockCommand

        elif operation == "stockgroupedbyshop":
            stockGroupedByShopCommand = SearchStockByShopId()
            return stockGroupedByShopCommand

        elif operation == "changeprice":
            changepriceCommand = PriceCalculator()
            return changepriceCommand
