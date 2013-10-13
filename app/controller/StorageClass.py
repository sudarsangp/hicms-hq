
'''
    This class will retrieve data from the database which inturn is represented
     by the SQL-alchemy classes.
     
'''

from app.model.models import db, Customer,Shops, Location, Manufacturers,Category,Products, Stock
from flask import session

class StorageClass(object):
    
    def addCustomerTODatabase(self,formData):
        newCustomerData = Customer(formData.customername.data,formData.customeraddress.data,
                                   formData.handphone.data,formData.customerId.data,formData.dateofjoining.data,
                                   formData.passwordcustomer.data)
    
        db.session.add(newCustomerData)
        try:
        	db.session.commit()
        except Exception as e:
        	#log data
        	# this part need to check whether exception works
        	db.session.flush()
        	raise e


    def query_database(self, formData):
    	idQuery = Customer.query.filter_by(customerId = formData.customerId.data).first()
    	if idQuery:
    		# email already present in database
    		return False
    	else:
    		return True
 
    def addManufacturerToDatabase(self,formData):
      #  newManufacturerData = Manufacturers(formData.manufacturerId.data, formData.name.data, formData.isContractValid.data) 
        newManufacturerData = Manufacturers(formData.manufacturerId.data, formData.mname.data, True) 
        #isManufacturerIdPresent
        
        db.session.add(newManufacturerData) 
        db.session.commit()
        # need to check if data is being added to database automatically
        #db.session.flush()
        #db.session.refresh(newCustomerData)
        #db.session.close()
        #return "from StorageClass"

    def addShopTODatabase(self,formData):
        newShopData = Shops(formData.shopId.data, formData.city.data, formData.country.data,
                            formData.address.data, formData.admin.data, formData.contactNumber.data)
        db.session.add(newShopData)
        db.session.commit()

    def shop_query_database(self, formData):
        shopidquery = Shops.query.filter_by(shopId = formData.shopId.data).first()
        if shopidquery:
            return False
        else:
            return True

    def check_if_manufacturer_not_exists(self,newManufacturerId):
        manufacturer_id = Manufacturers.query.filter_by( manufacturerId = newManufacturerId).first()
        
        if manufacturer_id:
            return False
        else:
            return True
    
    def addCategoryToDatabase(self,formData):
        newManufacturerData = Category(formData.categoryId.data, formData.categoryDescription.data,formData.isExpirable.data)
        
        db.session.add(newManufacturerData) 
        db.session.commit()    

    def addStockToDatabase(self, formData):
        newStockData = Stock(formData.barcode.data, formData.serialNumber.data, formData.batchQty.data, formData.isOnDisplay.data)

        db.session.add(newStockData)
        db.session.commit()

    def check_if_stock_exists(self, formData):
       #if dropdown for serial number then no need to check
        serialNumber = Stock.query.filter_by(serialNumber = formData.serialNumber.data).first()

        if serialNumber:
            return False
        else:
            return True
               
    def add_location_to_database(self, formData):
        newLocationData = Location(formData.city.data, formData.country.data, 
                                    formData.tax.data, formData.distance.data)
        db.session.add(newLocationData)
        db.session.commit()

    def location_query_database(self, formData):
        cityquery = Location.query.filter_by(city = formData.city.data).first()
        countryquery = Location.query.filter_by(country = formData.country.data).first()
        if cityquery and countryquery:
            return False
        else:
            return True
            
    def get_all_location(self, fromData):
        existinglocation = Location.query.all()
        return existinglocation

    def check_if_category_not_exists(self,newCategoryId):
        category_id = Category.query.filter_by( categoryId = newCategoryId).first()
        
        if category_id:
            return False
        else:
            return True
    
    def addProductToDatabase(self,formData):
        newProductData = Products(formData.barcode.data,formData.proname.data,formData.manufacturerId.data,formData.category.data,formData.price.data,
                                  formData.minStock.data,formData.currentStock.data,formData.bundleUnit.data,formData.displayPrice.data,formData.displayQty.data)

        db.session.add(newProductData) 
        db.session.commit()  
    
    def check_if_Product_exists(self,formData):
        product_id = Products.query.filter_by( barcode = formData.barcode.data).first()
        
        if product_id:
            return False
        else:
            return True    

    def check_if_Shop_exists(self,formData):
        shop_id = Shops.query.filter_by( shopId = formData.shopId.data).first()
        
        if shop_id:
            return True
        else:
            return False

    def get_manufacturers_from_db(self,formData):
        existingManufacturers = Manufacturers.query.all()
        return existingManufacturers    
    
    def get_categories_from_db(self,formData):
        existingCategories = Category.query.all()
        return existingCategories    

    def get_products_from_db(self):
        existingProduct = Products.query.all()
        return existingProduct

    def get_stock_quantity_for_barcode(self, enteredBarcode):
        stockData = Stock.query.filter_by(barcode = enteredBarcode).first()
        return stockData.batchQty
    
    def set_stock_quantity_for_barcode(self, enteredBarcode, quantity):
        stockData = Stock.query.filter_by(barcode = enteredBarcode).first()
        stockData.batchQty = quantity
        db.session.commit()

    def get_product_for_barcode(self,enteredBarcode):
        existingProduct = Products.query.filter_by(barcode = enteredBarcode).first()
        return existingProduct

    def get_shops_from_db(self):
        existingShops = Shops.query.all()
        return existingShops
    
    def get_shop_shopid_from_db(self, enteredShopId):
        existingShopForShopId = Shops.query.filter_by(shopId = enteredShopId).first()
        return existingShopForShopId

    def set_shop_details(self, formData):

        updateshop = Shops.query.filter_by(shopId = formData.shopId.data).first()
        updateshop.address = formData.address.data
        updateshop.admin = formData.admin.data
        updateshop.contactNumber = formData.contactNumber.data
        db.session.commit()

    def delete_shop_info(self, enteredShopId):
        shoptodelete = Shops.query.filter_by(shopId = enteredShopId).first()
        db.session.delete(shoptodelete)
        db.session.commit()
        
