
'''
    This class will retrieve data from the database which inturn is represented
     by the SQL-alchemy classes.
     
'''

from app.model.models import db, Customer,Shops, Location, Manufacturers,Category,Products, Stock, SoldStock
from flask import session
from Feedback import Feedback
from ast import literal_eval
import os

fname = 'newitems.txt'

class StorageClass(object):
    
    def __init__(self):
        self.feedbackObject = Feedback()

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
        newManufacturerData = Manufacturers(formData.manufacturerId.data, formData.mname.data, False) 
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
        newManufacturerData = Category(formData.categoryId.data, formData.categoryDescription.data,0)#hard code here
        
        db.session.add(newManufacturerData) 
        db.session.commit()    

    def addStockToDatabase(self, formData):
        newStockData = Stock(formData.barcode.data, formData.shopId.data, formData.stockQty.data)
        db.session.add(newStockData)
        db.session.commit()

    def check_if_stock_exists(self, formData):
        barcodeshop = Stock.query.filter_by(barcode = formData.barcode.data, shopId = formData.shopId.data).first()
        if barcodeshop:
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

    def get_stock_from_db(self):
        existingStock = Stock.query.all()
        return existingStock

    def get_stock_grouped_shopId(self, enteredShopId):
        stockbyshopid = Stock.query.filter_by(shopId = enteredShopId).all()
        return stockbyshopid

    """def priceCalculator(self,enteredBarcode):
        totalCurrentStock = 0;
        temptotalCurrentStock = Stock.query.filter(Stock.barcode == enteredBarcode).all()
        for row in temptotalCurrentStock :
            totalCurrentStock += row.stockQty
        totalshops = Shops.query.distinct(Shops.shopId).count()
        productToCalculate = Products.query.filter_by(barcode = enteredBarcode).first()
        oldPrice = productToCalculate.price
        totalMinStock = totalshops * productToCalculate.minStock
        #print type(oldPrice)
        #print oldPrice 
        if totalshops == 0:
            self.feedbackObject.setinfo("Sorry there are no shops")
        elif productToCalculate.minStock == 0:
            self.feedbackObject.setinfo("minStock is zero. Please check inventory")
         
        else:

            newPrice = oldPrice*(1-(((totalCurrentStock-totalMinStock)/totalMinStock)*0.05))    
            productToCalculate.price = newPrice
            self.feedbackObject.setdata(newPrice)
            self.feedbackObject.setcommandtype("Active Price")
            self.feedbackObject.setinfo("Success: oldprice :" + str(oldPrice) + " newprice:" + str(newPrice))
            #db.session.add(productToCalculate)
            #db.session.commit()
            #print totalshops
            #print totalCurrentStock
            #print totalMinStock
            #print newPrice
            newPrice = 0.05*round(newPrice/0.05)
            newPrice = int(newPrice*100)/100.0
            return newPrice"""

    def all_barcode_acitve_price(self, shopidin):
        bar_price = []
        newfilename = 'changestock.txt'
        if os.stat(newfilename)[6] == 0:
            bar_price_dict = {'barcode':'None','newprice':'no price'}
            bar_price.append(bar_price_dict)
            #print bar_price
            return bar_price
        try:
            with open(newfilename):
                f = open(newfilename,"r")
                contentdata = f.read()
                list_content = contentdata.split(';')
                del list_content[0]
                
                for eachvalue in list_content:
                    
                    stockvalue = literal_eval(eachvalue)
                    
                    stockcontent = stockvalue['updatestock']
                    barcodevalue = stockcontent['barcode']
                    shopidvalue = stockcontent['shopid']
                    newprice = self.active_price_calculator(barcodevalue,shopidvalue)
                    dict_bar_price = {'barcode':barcodevalue,'newprice':newprice}
                    bar_price.append(dict_bar_price)
                #open(newfilename, 'w').close()
        except IOError:
          bar_price = {'update':'No file'}  
        #for oneprod in Products.query.all():
            #newprice = self.active_price_calculator(oneprod.barcode,1) # change this to shopid and do for unique product
            #dict_bar_price = {'barcode':oneprod.barcode,'newprice':newprice}
            #bar_price.append(dict_bar_price)
        return bar_price

    def update_stock(self, formData):
        existingStock = Stock.query.filter_by(barcode = formData.barcode.data , shopId = formData.shopId.data).first()
        if existingStock.stockQty != int(formData.stockQty.data):
            fObject = open('changestock.txt', 'a')
            prodall = {}
            textprod = {}
            textprod['barcode'] = formData.barcode.data
            textprod['shopid'] = formData.shopId.data
            textprod['stockqty'] = formData.stockQty.data
            prodall['updatestock'] = textprod
            fObject.write(";")
            fObject.write(str(prodall))
            fObject.close()
        existingStock.stockQty = formData.stockQty.data
        db.session.commit()

    def active_price_calculator(self, enteredBarcode, shopidin):
        productDetail = Products.query.filter_by(barcode = enteredBarcode).first()
        costprice = productDetail.price
        minStockQty = productDetail.minStock
        stockDetail = Stock.query.filter_by(barcode = enteredBarcode).filter_by(shopId = shopidin).first()
        currentStock = stockDetail.stockQty
        numerator = 50 + (1.093 ** costprice)
        denominator = currentStock - (0.9*minStockQty)
        active_price = costprice + (numerator/denominator)
        active_price = 0.05*round(active_price/0.05)
        active_price = int(active_price*100)/100.0
        stockDetail.lastActivePrice = active_price
        print active_price, enteredBarcode
        db.session.commit()
        return active_price