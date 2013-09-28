from app import db
from werkzeug import generate_password_hash, check_password_hash

class Customer(db.Model):

  __tablename__ = "customer"

  name = db.Column(db.String(256))
  address = db.Column(db.String(256))
  hp = db.Column(db.Integer)
  email = db.Column(db.String, primary_key = True)
  dateOfJoining = db.Column(db.Date)
  points = db.Column(db.Integer)
  password = db.Column(db.String(256))

  def __init__(self,name, address, hp, email, dateOfJoining, password):
      self.name = name
      self.address = address
      self.hp = hp
      self.email = email
      self.dateOfJoining = dateOfJoining
      self.points = 0
      self.password = password

class Category(db.Model):
    __tablename__ = "Category"
    
    categoryId = db.Column(db.String(256),primary_key= True) 
    categoryDescription = db.Column(db.String(256),nullable = False)
    isExpirable = db.Column(db.Boolean,nullable = False)
    
    def __init__(self,categoryId,categoryDescription,isExpirable):
        self.categoryDescription = categoryDescription
        self.categoryId = categoryId
        self.isExpirable = isExpirable    

class Manufacturers(db.Model):    
    
  __tablename__ = "Manufacturers"
  
  manufacturerId = db.Column(db.String(256),primary_key= True)  
  name = db.Column(db.String(256),nullable = False)
  isContractValid = db.Column(db.Boolean,nullable = False)
  
  def __init__(self,manufacturerId,name,isContractValid):
       self.manufacturerId = manufacturerId 
       self.name = name
       self.isContractValid = isContractValid 

class Products(db.Model):
    __tablename__= "Products"  
    
    barcode = db.Column(db.String(256),primary_key= True)
    name = db.Column(db.String(256),nullable = False)
    manufacturerId = db.Column(db.String(256),nullable = False)
    category = db.Column(db.String(256),nullable = False)
    price = db.Column(db.Float,nullable = False)
    minStock = db.Column(db.Integer,nullable = False)
    currentStock = db.Column(db.Integer,nullable = False)
    bundleUnit = db.Column(db.Integer,nullable = False)
    displayPrice = db.Column(db.Float,nullable = False)
    displayQty = db.Column(db.Integer,nullable = False)

    def __init__(self,barcode,name,manufacturerId,category,price,minStock,currentStock,bundleUnit,displayPrice,displayQty):
       self.barcode = barcode 
       self.name = name
       self.manufacturerId = manufacturerId
       self.category = category
       self.price = price
       self.minStock = minStock
       self.currentStock = currentStock
       self.bundleUnit = bundleUnit
       self.displayPrice = displayPrice
       self.displayQty = displayQty
       

""" nets tuts tutorial flask login """
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

""" this one from flask documentation """
#class User(db.Model):
#	id = db.Column(db.Integer, primary_key = True)
#	name = db.Column(db.String(64), index = True, unique = True)
#	
#	def is_authenticated(self):
#		return True
#
#	def is_active(self):
#		return True
#
#	def is_anonymous(self):
#		return False
#
#	def get_id(self):
#		return unicode(self.id)


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