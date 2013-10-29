
'''
    This class will retrieve data from the database which inturn is represented
     by the SQL-alchemy classes.
     
'''

from app.model.models import db, Customer,Shops, Location, Manufacturers,Category,Products, Stock, SoldStock
from flask import session

fname = 'newitems.txt'

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
        newStockData = Stock(formData.barcode.data, formData.shopId.data, formData.stockQty.data)
        db.session.add(newStockData)
        db.session.commit()

    def check_if_stock_exists(self, formData):
        barcode = Stock.query.filter_by(barcode = formData.barcode.data).first()
        if barcode:
            return True
        else:
            return False

    def add_sold_stock_to_database(self,formData):
        newSoldStockData = SoldStock(formData.barcode.data, formData.priceSold.data, formData.unitSold.data, formData.shopId.data, formData.timeStamps.data)
        db.session.add(newSoldStockData)
        db.session.commit()

    def check_if_sold_stock_exists(self, formData):
        #counter = SoldStock.query.filter_by(barcode = formData.barcode.data).count()
        #if counter > 0:
        barcode = SoldStock.query.filter_by(barcode = formData.barcode.data).first()
        if barcode:
            return True
        else:
            return False
        #else:
        #   return False

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
                                  formData.minStock.data,formData.cacheStockQty.data,formData.bundleUnit.data)
        f = open(fname,'a')
        prodall = {}
        textprod = {}
        textprod['barcode'] = formData.barcode.data
        textprod['proname'] = formData.proname.data
        textprod['manufacturerId'] = formData.manufacturerId.data
        textprod['category'] = formData.category.data
        textprod['price'] = formData.price.data
        textprod['minStock'] = formData.minStock.data
        textprod['bundleUnit'] = formData.bundleUnit.data
        prodall['addproducts'] = textprod
        db.session.add(newProductData) 
        db.session.commit()
        f.write(";")
        f.write(str(prodall))
        f.close()

    def check_if_Product_exists(self,formData):
        product_id = Products.query.filter_by( barcode = formData.barcode.data).first()
        #logic is inverted here
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
    
    def set_product_details(self, formData):
        flag = 0
        updateproduct = Products.query.filter_by(barcode = formData.barcode.data).first()
        if updateproduct.price == float(formData.price.data):
            if updateproduct.minStock == long(formData.minStock.data):
                if updateproduct.bundleUnit == long(formData.bundleUnit.data):
                    flag = 1
        #print type(updateproduct.price), type(formData.price.data)
        #print  type(updateproduct.minStock) ,type(formData.minStock.data)
        #print type(updateproduct.bundleUnit) ,type(formData.bundleUnit.data)
        #print flag
        updateproduct.price = formData.price.data
        updateproduct.minStock = formData.minStock.data
        updateproduct.cacheStockQty = formData.cacheStockQty.data
        updateproduct.bundleUnit = formData.bundleUnit.data
        db.session.commit()
        if flag == 0:
            f = open(fname,'a')
            prodall = {}
            textprod = {}
            textprod['barcode'] = formData.barcode.data
            textprod['price'] = formData.price.data
            textprod['minStock'] = formData.minStock.data
            textprod['bundleUnit'] = formData.bundleUnit.data
            prodall['editproducts'] = textprod
            f.write(";")
            f.write(str(prodall))
            f.close()

    def delete_product_info(self, enteredBarcode):
        allstockforbarcode = Stock.query.filter_by(barcode = enteredBarcode).all()
        for i in range(len(allstockforbarcode)):
            if allstockforbarcode[i].stockQty > 0:
                return False
        producttodelete = Products.query.filter_by(barcode = enteredBarcode).first()
        db.session.delete(producttodelete)
        db.session.commit()

        f = open(fname,'a')
        prodall = {}
        textprod = {}
        textprod['barcode'] = enteredBarcode
        prodall['deleteproducts'] = textprod
        f.write(";")
        f.write(str(prodall))
        f.close()

        return True

    def get_soldstock_from_db(self):
        existingSoldStocks = SoldStock.query.all()
        return existingSoldStocks

    def get_transaction_grouped_shopId(self, enteredShopId):
        transactionsbyshopid = SoldStock.query.filter_by(shopId = enteredShopId).all()
        return transactionsbyshopid

    def get_cachestockqty_from_product(self,formData):
        existingprod = Products.query.filter_by(barcode = formData.barcode.data).first()
        #print formData.quantity.data, type(formData.quantity.data)
        #print existingprod.cacheStockQty, type(existingprod.cacheStockQty)
        if long(formData.quantity.data) <=  existingprod.cacheStockQty:
            existingprod.cacheStockQty -= long(formData.quantity.data)
            db.session.commit()
            return formData.quantity.data
        else:
            return -2