from app import db
from werkzeug import generate_password_hash, check_password_hash

class Customer(db.Model):

  __tablename__ = "customer"

  name = db.Column(db.String(256))
  address = db.Column(db.String(256))
  hp = db.Column(db.Integer)
  customerId = db.Column(db.String, primary_key = True)
  dateOfJoining = db.Column(db.Date)
  points = db.Column(db.Integer)
  password = db.Column(db.String(256))

  def __init__(self,name, address, hp, customerId, dateOfJoining, password):
    self.name = name
    self.address = address
    self.hp = hp
    self.customerId = customerId
    self.dateOfJoining = dateOfJoining
    self.points = 0
    self.password = password
  
class Shops(db.Model):

  __tablename__ = "shops"

  shopId = db.Column(db.String(50), primary_key = True)
  city = db.Column(db.String(256))
  country = db.Column(db.String(256))
  address = db.Column(db.String(256))
  admin = db.Column(db.String(256))
  contactNumber = db.Column(db.Integer)

  def __init__(self,shopId, city, country, address, admin, contactNumber):
    self.shopId = shopId
    self.city = city
    self.country = country
    self.address = address
    self.admin = admin
    self.contactNumber = contactNumber
 
class Location(db.Model):

  __tablename__ = "location"

  city = db.Column(db.String(256), primary_key = True)
  country = db.Column(db.String(256), primary_key = True)
  tax = db.Column(db.Float)
  distance = db.Column(db.Float)

  def __init__(self, city, country, tax, distance):
    self.city = city
    self.country = country
    self.tax = tax
    self.distance = distance

class Stock(db.Model):

  __tablename__ = "stock"

  barcode = db.Column(db.String(256), primary_key = True)
  shopId = db.Column(db.String(256), primary_key = True)
  stockQty = db.Column(db.Integer)
  lastActivePrice = db.Column(db.Float, nullable = False)

  def __init__(self, barcode, shopId, stockQty):
    self.barcode = barcode
    self.shopId = shopId
    self.stockQty = stockQty
    self.lastActivePrice = 0

class SoldStock(db.Model):

  __tablename__ = "soldstock"

  barcode = db.Column(db.String(256), primary_key = True)
  priceSold = db.Column(db.Float,nullable = False)
  unitSold = db.Column(db.Integer,nullable = False)
  shopId = db.Column(db.String(256),primary_key = True)
  timeStamps = db.Column(db.TIMESTAMP,primary_key = True)

  def __init__(self, barcode, priceSold, unitSold, shopId, timeStamp):
    self.barcode = barcode
    self.priceSold = priceSold
    self.unitSold = unitSold
    self.shopId = shopId
    self.timeStamps = timeStamp

class Category(db.Model):
    __tablename__ = "category"
    
    categoryId = db.Column(db.String(256),primary_key= True) 
    categoryDescription = db.Column(db.String(256),nullable = False)
    isExpirable = db.Column(db.Boolean,nullable = False)
    
    def __init__(self,categoryId,categoryDescription,isExpirable):
        self.categoryDescription = categoryDescription
        self.categoryId = categoryId
        self.isExpirable = 0    


class Manufacturers(db.Model):    
    
  __tablename__ = "manufacturers"
  
  manufacturerId = db.Column(db.String(256),primary_key= True)  
  name = db.Column(db.String(256),nullable = False)
  isContractValid = db.Column(db.Boolean,nullable = False)
  
  def __init__(self,manufacturerId,name,isContractValid):
       self.manufacturerId = manufacturerId 
       self.name = name
       self.isContractValid = 0

class Products(db.Model):
    __tablename__= "products"  
    
    barcode = db.Column(db.String(256),primary_key= True)
    name = db.Column(db.String(256),nullable = False)
    manufacturerId = db.Column(db.String(256),nullable = False)
    category = db.Column(db.String(256),nullable = False)
    price = db.Column(db.Float,nullable = False)
    minStock = db.Column(db.Integer,nullable = False)
    cacheStockQty = db.Column(db.Integer,nullable = False)
    bundleUnit = db.Column(db.Integer,nullable = False)
    

    def __init__(self,barcode,name,manufacturerId,category,price,minStock,cacheStockQty,bundleUnit):
       self.barcode = barcode 
       self.name = name
       self.manufacturerId = manufacturerId
       self.category = category
       self.price = price
       self.minStock = minStock
       self.cacheStockQty = cacheStockQty
       self.bundleUnit = bundleUnit
       
       
class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
   
  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

""" to ensure whetehr database connection works """
class Check(db.Model):
	id_check = db.Column(db.Integer,primary_key=True)
	fullname = db.Column(db.String(80))

	def check_id(self):
		checklist = []
		all_query = Check.query.all()
		for x in range(len(all_query)):
			checklist.append(all_query[x].id_check)
		return str(checklist)