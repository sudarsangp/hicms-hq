from flask import render_template, flash, request, session, redirect, url_for, jsonify
from flask.ext.login import login_required
from app import app, login_manager

from form.forms import RegisterShopForm, SignupForm, SigninForm, ShopAdminFunction, AddCustomer ,AddManufacturer , AddStock, AddCategory, AddProduct, BuyItem
from form.forms import SearchBarcode, LocationShopForm, HQAdminFunction, RetrieveShop, UpdateShopForm, UpdateProductForm, StockForm, SoldStockForm

from model.models import Check, User, db, Customer
from controller import Logic

import requests, json, time, datetime
from ast import literal_eval

@app.route('/check')
def default():
  return render_template("baselayout.html")



#############################################################################################
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if 'email' in session:
  	return redirect(url_for('profile')) 

  if request.method == 'POST':
    if form.validate() == False:
    	return render_template('signup.html', form=form)
    else:
    	newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      	db.session.add(newuser)
      	db.session.commit()
      	session['email'] = newuser.email
     	return redirect(url_for('profile'))
   
  elif request.method == 'GET':
  	return render_template('signup.html', form=form)

@app.route('/')
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  
  if 'email' in session:
    return redirect(url_for('profile'))  

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('hq_functions'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form) 

@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))

  session.pop('email', None)
  return redirect(url_for('signin'))

@app.route('/profile')
def profile():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html')
##############################################################################################

@app.route('/hq', methods = ['POST', 'GET'])
def hq_functions():
  form = HQAdminFunction()
  if request.method == "POST":
    operation = form.operations.data

    if operation == "addshop":
      return redirect(url_for('addshop', operation = operation))   
    
    elif operation == "retrieveshop":
      return redirect(url_for('retrieve_shop', operation = operation))

    elif operation == "updateshop":
      return redirect(url_for('update_shop', operation = operation))

    elif operation == "deleteshop":
      return redirect(url_for('delete_shop', operation = operation))

    elif operation == "viewshops":
      return redirect(url_for('view_all_shops', operation = operation))
     
    elif operation == "addproduct":
      return redirect(url_for('addproduct',operation = operation))  

    elif operation == "retrieveproduct":
      return redirect(url_for('retrieve_product', operation = operation))

    elif operation == "updateproduct":
      return redirect(url_for('update_product', operation = operation))

    elif operation == "deleteproduct":
      return redirect(url_for('delete_product', operation = operation))

    elif operation == "viewproducts":
      return redirect(url_for('view_all_products',operation = operation))

    elif operation == "addlocation":
      return redirect(url_for('enterlocation', operation = operation))   

    elif operation == "sendinventory":
      return redirect(url_for('send_inventory', operation = operation))

    else:
      print operation
      return "Mapping not yet implemented"
  elif request.method == "GET":
    return render_template('HQshop_related_operation.html', form = form)

@app.route('/sendinventory/<operation>', methods = ['POST','GET'])
def send_inventory(operation):
  logicObject = Logic.Logic()
  feedback = logicObject.execute(operation,None)
  return render_template('feedback.html', feedback = feedback)

@app.route('/deleteproduct/<operation>', methods = ['POST', 'GET'])
def delete_product(operation):
  form = SearchBarcode()
  if request.method == "POST":
    logicObject = Logic.Logic()
    feedback = logicObject.execute(operation, form)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == 'GET':
    return render_template('searchbarcode.html',form = form)

@app.route('/updateproduct/<operation>', methods = ['POST', 'GET'])
def update_product(operation):
  form = SearchBarcode()
  if request.method == "POST":
    formbarcode = form.barcode.data
    return redirect(url_for('actual_updateproduct', formbarcode = formbarcode))

  elif request.method == 'GET':
    return render_template('searchbarcode.html', form = form)

@app.route('/toupdateproduct/<formbarcode>', methods = ['POST', 'GET'])
def actual_updateproduct(formbarcode):
  updateproductinfo = UpdateProductForm()
  logicObject = Logic.Logic()
  if request.method == "POST":
    updateproductinfo.barcode.data = formbarcode
    feedback = logicObject.execute("updateproduct", updateproductinfo)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == 'GET':
    
    updateproductinfo.barcode.data = formbarcode
    retrieveproductinfo = logicObject.execute("retrieveproduct", updateproductinfo)
    if retrieveproductinfo:
      updateproductinfo.barcode = retrieveproductinfo.barcode
      updateproductinfo.proname = retrieveproductinfo.name
      updateproductinfo.manufacturerId = retrieveproductinfo.manufacturerId
      updateproductinfo.category = retrieveproductinfo.category
      updateproductinfo.price.data = retrieveproductinfo.price
      updateproductinfo.minStock.data = retrieveproductinfo.minStock
      updateproductinfo.cacheStockQty.data = retrieveproductinfo.cacheStockQty
      updateproductinfo.bundleUnit.data = retrieveproductinfo.bundleUnit
      
      return render_template('updateproductforbarcode.html', updateproductinfo = updateproductinfo)

    else:
      return redirect(url_for('defaulterror'))
      
@app.route('/retrieveproduct/<operation>', methods = ['POST', 'GET'])
def retrieve_product(operation):
  return redirect(url_for('search_barcode', operation = operation))

@app.route('/deleteshop/<operation>', methods = ['POST', 'GET'])
def delete_shop(operation):
  form = RetrieveShop()
  if request.method == "POST":
    logicObject = Logic.Logic()
    feedback = logicObject.execute(operation, form)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == 'GET':
    return render_template('retrieveshopId.html',form = form)

@app.route('/updateshop/<operation>', methods = ['POST','GET'])
def update_shop(operation):
  form = RetrieveShop()
  if request.method == "POST":
    
    formshopid = form.shopId.data
    return redirect(url_for('check_update',formshopid = formshopid ))

  elif request.method == 'GET':
    return render_template('retrieveshopId.html',form = form)

@app.route('/tocheckupdate/<formshopid>', methods = ['POST', 'GET'])
def check_update(formshopid):
  updateshopinfo = UpdateShopForm()
  logicObject = Logic.Logic()
  if request.method == "POST":
    updateshopinfo.shopId.data = formshopid
    feedback = logicObject.execute("updateshop", updateshopinfo)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == 'GET':
    
    updateshopinfo.shopId.data = formshopid
    retrievehopinfo = logicObject.execute("retrieveshop", updateshopinfo)
    if retrievehopinfo:
      updateshopinfo.shopId = retrievehopinfo.shopId
      updateshopinfo.city = retrievehopinfo.city
      updateshopinfo.country = retrievehopinfo.country
      updateshopinfo.address.data = retrievehopinfo.address
      updateshopinfo.admin.data = retrievehopinfo.admin
      updateshopinfo.contactNumber.data = retrievehopinfo.contactNumber
      return render_template('updateshopforshopId.html', updateshopinfo = updateshopinfo)

    else:
      return redirect(url_for('defaulterror'))

@app.route('/retrieveshop/<operation>', methods = ['POST','GET'])
def retrieve_shop(operation):
  form = RetrieveShop()
  if request.method == "POST":
    logicObject = Logic.Logic()
    singleshop = logicObject.execute(operation,form)
    if singleshop:
      return render_template('shopdetailsforshopId.html', singleshop = singleshop)
    else:
      return redirect(url_for('defaulterror'))

  elif request.method == 'GET':
    return render_template('retrieveshopId.html',form = form)
  
@app.route('/displayshops/<operation>')
def view_all_shops(operation):
  logicObject = Logic.Logic()
  allshops = logicObject.execute(operation, None)
  return render_template('listingshops.html', allshops = allshops)

@app.route('/location/<operation>', methods = ['POST', 'GET'])
def enterlocation(operation):
  form = LocationShopForm()
  if request.method == "POST":
    
    logicObject = Logic.Logic()
    feedback = logicObject.execute(operation, form)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == "GET":
    return render_template('shoplocation.html', form = form)

@app.route('/shop/<operation>', methods = ['POST', 'GET'])
def addshop(operation):
  logicObject = Logic.Logic()
  locationsall = logicObject.execute('viewlocation',None)
  location_choices_city = [(locationobj.city, locationobj.city) for locationobj in locationsall]
  location_choices_country = [(locationobj.country, locationobj.country) for locationobj in locationsall]

  
  #location_choices_city, location_choices_country = [(locationobj.city,locationobj.city),(locationobj.country,locationobj.country) for locationobj in locationsall]
  location_choices_city.append(('-1','None'))
  location_choices_country.append(('-1', 'None'))
  form = RegisterShopForm()
  form.city.choices = location_choices_city
  form.country.choices = location_choices_country
  if request.method == "POST": 
    
    if form.city.data == "none" or form.country.data == "none" :
      logicObject.execute("addlocation",form.emformlocation)
      form.city.data = form.emformlocation.city.data
      form.country.data = form.emformlocation.country.data
    feedback = logicObject.execute(operation, form)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == "GET":    
    return render_template('registershop.html',form = form)

@app.route('/productsearch/<operation>', methods = ['POST','GET'])
def search_barcode(operation):
  form = SearchBarcode()
  if request.method == "POST":
    logicObject = Logic.Logic()
    productobj = logicObject.execute(operation,form)
    if productobj:
      return render_template('productdetailsforbarcode.html', productobj = productobj)
    else:
      return redirect(url_for('defaulterror'))

  elif request.method == 'GET':
    return render_template('searchbarcode.html',form = form)

@app.route('/productdisplayall/<operation>')
def view_all_products(operation):
  logicObject = Logic.Logic()
  allproducts = logicObject.execute(operation, None)
  return render_template('listinginventory.html', allproducts = allproducts)

@app.route('/customer/<operation>', methods = ['POST', 'GET'])
#@login_required
def addcustomer(operation):
 
  form = AddCustomer()
  if request.method ==  "POST" and form.validate():
  
    logicObject = Logic.Logic()
    feedback = logicObject.execute(operation,form)
    return render_template('feedback.html', feedback = feedback)
    
  elif request.method == 'GET':
    return render_template('addcustomer.html', form = form)


@app.route('/manufacturer/<operation>', methods = ['POST', 'GET'])
#@login_required    
def addmanufacturer(operation):
	
	form = AddManufacturer()
	if request.method == "POST":
	
		logicObject = Logic.Logic()
		feedback = logicObject.execute(operation,form)
		return render_template('feedback.html',feedback = feedback)
	
	elif request.method == 'GET':
		return render_template('addmanufacturer.html', form = form)	

@app.route('/category/<operation>', methods = ['POST', 'GET'])
#@login_required
def addcategory(operation):
	
	form = AddCategory()
	if request.method == "POST":
	
		logicObject = Logic.Logic()
		feedback = logicObject.execute(operation,form)
		return render_template('feedback.html',feedback = feedback)
	
	elif request.method == 'GET':
		return render_template('addcategory.html', form = form)	
	
@app.route('/productadd/<operation>', methods = ['POST', 'GET'])
#@login_required    
def addproduct(operation):
	
	logicObject = Logic.Logic()
	manufacturers = logicObject.execute('viewmanufacturers',None)
	manufacturer_choices = [(manufacturer.manufacturerId,manufacturer.name) for manufacturer in manufacturers]
	manufacturer_choices.append(('-1','None'))
	categories = logicObject.execute('viewcategories',None)
	category_choices =[(category.categoryId,category.categoryDescription) for category in categories]
	category_choices.append(('-1','None'))
	
	form = AddProduct()	
	form.manufacturerId.choices = manufacturer_choices
	form.category.choices = category_choices
	if request.method == "POST":
		if(form.manufacturerId.data == '-1'):
			form.manufacturerId.data = form.manufacturerForm.manufacturerId.data
			feedback = logicObject.execute('addmanufacturer',form.manufacturerForm)
			if(feedback.getinfo() != "Success: data added "):
				return render_template('feedback.html',feedback = feedback)
		
		if(form.category.data == '-1'):
			form.category.data = form.categoryForm.categoryId.data	
			feedback = logicObject.execute('addcategory',form.categoryForm)
			if(feedback.getinfo() != "Success: data added "):
				return render_template('feedback.html',feedback = feedback)	
		
		
		feedback = logicObject.execute(operation,form)
		
		return render_template('feedback.html',feedback = feedback)
	
	elif request.method == 'GET':
		return render_template('addproduct.html', form = form)
	
	
@app.route('/stockadd/<operation>', methods = ['POST', 'GET'])
#@login_required
def addstock(operation):

  logicObject = Logic.Logic()
  products = logicObject.execute('viewproducts', None)
  product_choices = [(prod.barcode,prod.barcode) for prod in products]
  product_choices.append(('-1','None'))

  form = AddStock()
  form.barcode.choices = product_choices
  if request.method == 'POST':
    
    feedback = logicObject.execute(operation, form)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == 'GET':
    return render_template('addstock.html', form = form)

@app.route('/user', methods = ['POST', 'GET'])
def buyitem():
  form = BuyItem()
  if request.method == 'POST':
    logicObject = Logic.Logic()
    feedback = logicObject.execute('buyitem',form)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == 'GET':
    return render_template('buyitem.html', form=form)

@app.route('/defaulterror')
def defaulterror():
  return "Data not present"

#to check the database part works fine
@app.route('/db')
def db_check():
	checkdb = Check()
	return checkdb.check_id()


#to check server information
@app.route('/serverinfo', methods = ['POST']) 
def server_info():
  stock_soldstock = request.data
  stock_soldstock_dict = json.loads(stock_soldstock)
  stock_info = {}
  soldstock_info = {}
  stock_list = stock_soldstock_dict['Stock']
  soldstock_list = stock_soldstock_dict['SoldStock']

  stock_form = StockForm()
  soldstock_form = SoldStockForm()
  logicObject = Logic.Logic()
 
  for i in range(len(stock_list)):
    stock_info = literal_eval(json.dumps(stock_list[i]))
    stock_form.barcode.data = stock_info['Barcode']
    stock_form.shopId.data = stock_info['ShopId']
    stock_form.stockQty.data = stock_info['Stock']
    feedback = logicObject.execute('addstock',stock_form)

  for j in range(len(soldstock_list)):
    soldstock_info = literal_eval(json.dumps(soldstock_list[j]))
    soldstock_form.barcode.data = soldstock_info['Barcode']
    soldstock_form.priceSold.data = soldstock_info['priceSold']
    soldstock_form.unitSold.data = soldstock_info['unitSold']
    soldstock_form.shopId.data = soldstock_info['ShopId']
    soldstock_form.timeStamp.data = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    feedback = logicObject.execute('addsoldstock',soldstock_form)

  return str(stock_soldstock)
  