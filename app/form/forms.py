from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, BooleanField, TextAreaField, SubmitField, ValidationError, RadioField, DateField
from app.model.models import User

class LocationShopForm(Form):
  city = TextField('city', validators = [validators.Required()])
  country = TextField('country', validators = [validators.Required()])
  tax = TextField('tax', validators = [validators.Required()])
  distance = TextField('distance', validators = [validators.Required()])

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class RegisterShopForm(Form):
  shopId = TextField('shopId', validators = [validators.Required()])
  city = TextField('city', validators = [validators.Required()])
  country = TextField('country', validators = [validators.Required()])
  address = TextAreaField('address', validators = [validators.Required()])
  admin = TextField('admin', validators = [validators.Required()])
  contactNumber = TextField('contactNumber', validators = [validators.Required()])
    
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class ShopAdminFunction(Form):
  operations = RadioField('operations', choices = [('addproduct', 'Add Product'),('editproduct','Edit Product'),('removeproduct','Remove Product'),
                                                   ('addcustomer','Add Customer'),('editcustomer','Edit Customer'),('removecustomer','Remove Customer')])

class HQAdminFunction(Form):
  operations = RadioField('operations', choices = [('addshop','Add Shop')])


class AddCustomer(Form):
  customername = TextField('customername', validators = [validators.Required()])
  customeraddress = TextAreaField('customeraddress', validators = [validators.Required()])
  handphone = TextField('handphone', validators = [validators.Required()])
  emailid = TextField('emailid', validators = [validators.Required(), validators.Email("Please enter your email address.")])
  dateofjoining = DateField('dateofjoining', validators = [validators.Required()])
  passwordcustomer = PasswordField('passwordcustomer', validators = [validators.Required()])

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
