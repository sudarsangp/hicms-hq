from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, BooleanField, TextAreaField, SubmitField, ValidationError, RadioField, DateField, FormField, SelectField
from app.model.models import User

class LocationShopForm(Form):
  city = TextField('city', validators = [validators.Required()])
  country = TextField('country', validators = [validators.Required()])
  tax = TextField('tax', validators = [validators.Required()])
  distance = TextField('distance', validators = [validators.Required()])

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

import re

def validateNotEmpty(form,field):
  s = field.data
  s = s.replace(' ','')
  if len(s) == 0:
    raise ValidationError('Cannot give empty space')

def validateNumber(form,field):
  s = field.data
  if re.match("^\D+$",s):
    raise ValidationError('please enter only numbers')

class RegisterShopForm(Form):
  shopId = TextField('shopId', validators = [validators.Required()])
  city = SelectField('city', choices=[])
  country = SelectField('country', choices=[])
  emformlocation = FormField(LocationShopForm)
  address = TextAreaField('address', validators = [validators.Required()])
  admin = TextField('admin', validators = [validators.Required()])
  contactNumber = TextField('contactNumber', validators = [validators.Required()])
    
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class UpdateShopForm(Form):
  shopId = TextField('shopId', validators = [validators.Required()])
  city = TextField('city', validators = [validators.Required()])
  country = TextField('country', validators = [validators.Required()])
  address = TextAreaField('address', validators = [validators.Required()])
  admin = TextField('admin', validators = [validators.Required()])
  contactNumber = TextField('contactNumber', validators = [validators.Required()])

  def __init__(self, *args, **kwargs):
      Form.__init__(self, *args, **kwargs)

class RetrieveShop(Form):
  shopId = TextField('shopId')

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class ShopAdminFunction(Form):
  operations = RadioField('operations', choices = [('searchBarcode','Search Barcode'),('viewproducts','View Product')])

class HQAdminFunction(Form):
  operations = RadioField('operations', choices = [('addshop','Create Shop'),('retrieveshop', 'Retrieve Shop'),('updateshop','Update Shop'),('deleteshop','Delete Shop'),('viewshops','List All Shops'),
    ('addlocation','Add Location'),('addproduct','Add Product'),
    ('addcategory','Add Category'),('addmanufacturer','Add Manufacturer'),('addcustomer','Add Customer'),('addstock', 'Add Stock'),
    ('viewproducts','View All Products'),
    ('editproduct','Edit Product'),('editcustomer','Edit Customer'),
    ('removeproduct','Remove Product'),('removecustomer','Remove Customer')])

class AddCustomer(Form):
  customername = TextField('customername', validators = [validators.Required(), validateNotEmpty])
  customeraddress = TextAreaField('customeraddress', validators = [validators.Required(), validateNotEmpty ])
  handphone = TextField('handphone', validators = [validators.Required(), validateNotEmpty, validateNumber])
  customerId = TextField('customerId', validators = [validators.Required(), validateNotEmpty]) 
  dateofjoining = DateField('dateofjoining', validators = [validators.Required()])
  passwordcustomer = PasswordField('passwordcustomer', validators = [validators.Required()])
  
  def __init__(self, *args, **kwargs):
   Form.__init__(self, *args, **kwargs)

class AddManufacturer(Form):
  manufacturerId = TextField('manufacturerId',validators = [validators.Required("Please enter manufacturer Id"), validateNotEmpty])
  mname = TextField('name',validators = [validators.Required("Please enter manufacturer Name"), validateNotEmpty])
  isContractValid = TextField('isContractValid',validators = [validators.Required()])
	
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class AddCategory(Form):
  categoryId = TextField('categoryId',validators = [validators.Required(), validateNotEmpty])
  categoryDescription = TextField('categoryDescription',validators = [validators.Required(), validateNotEmpty])
  isExpirable = TextField('isExpirable',validators = [validators.Required()])
	
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)  
    
class AddProduct(Form):
  barcode = TextField('barcode',validators = [validators.Required(), validateNotEmpty, validateNumber])
  proname = TextField('name',validators = [validators.Required(), validateNotEmpty])
  manufacturerId = SelectField('manufacturerId',choices=[])
  manufacturerForm = FormField(AddManufacturer)
#  manufacturerId = TextField('manufacturerId',validators = [validators.Required()])
  category = SelectField('category',choices=[])
  categoryForm = FormField(AddCategory)
  price = TextField('price',validators = [validators.Required(), validateNotEmpty, validateNumber])
  minStock = TextField('minStock',validators = [validators.Required(), validateNotEmpty, validateNumber])
  currentStock = TextField('currentStock',validators = [validators.Required(), validateNotEmpty, validateNumber])
  bundleUnit = TextField('bundleUnit',validators = [validators.Required(), validateNumber, validateNotEmpty])
  displayPrice = TextField('displayPrice',validators = [validators.Required(), validateNumber, validateNotEmpty])
  displayQty = TextField('displayQty',validators = [validators.Required(), validateNumber, validateNotEmpty])
	
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)  
  
class AddStock(Form):
  barcode = SelectField('barcode', choices=[])
  serialNumber = TextField('serialNumber', validators = [validators.Required()])
  batchQty = TextField('batchQty', validators = [validators.Required()])
  isOnDisplay = BooleanField('isOnDisplay')

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class BuyItem(Form):
  barcode = TextField('barcode')
  quantity = TextField('quantity')

  def __init__(self, *args, **kwargs): # needed for importing in view.py
    Form.__init__(self, *args, **kwargs)

class SearchBarcode(Form):
  barcode = TextField('barcode')

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

################################################################################################################################################
class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True

class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False
#####################################################################################################################################################
