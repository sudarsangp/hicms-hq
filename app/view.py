from flask import render_template, flash, request, session, redirect, url_for, jsonify
from flask.ext.login import login_required
from app import app, login_manager

from form.forms import RegisterShopForm, SignupForm, SigninForm, ShopAdminFunction, AddCustomer ,AddManufacturer , AddStock, AddCategory, AddProduct, BuyItem
from form.forms import SearchBarcode, LocationShopForm, HQAdminFunction, RetrieveShop, UpdateShopForm, UpdateProductForm, StockForm, SoldStockForm, SearchShopId, PriceCalculator, SettingsForm

from model.models import Check, User, db, Customer
from controller import Logic
from controller.StorageClass import StorageClass

import requests, json, time, datetime
from ast import literal_eval
from operator import itemgetter

from config import POSTS_PER_PAGE

@app.route('/check')
def default():
  if 'email' not in session:
    return redirect(url_for('signin'))

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
  print user.uid 
  print user.firstname
  print user.lastname
  print user.email

  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html',user = user)
##############################################################################################

@app.route('/hq', methods = ['POST', 'GET'])
def hq_functions():
  if 'email' not in session:
    return redirect(url_for('signin'))

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
      return redirect(url_for('view_all_products',page = 1))

    elif operation == "addlocation":
      return redirect(url_for('enterlocation', operation = operation))   

    elif operation == "viewtransactions":
      return redirect(url_for('view_all_transaction', page = 1))

    elif operation == "transactiongroupedbyshop":
      return redirect(url_for('transaction_grouped_by_shop', operation = operation))

    elif operation == "viewstock":
      return redirect(url_for('view_stock', page = 1))

    elif operation == "stockgroupedbyshop":
      return redirect(url_for('stock_grouped_by_shop', page = 1))

    elif operation == "changeprice":
      return redirect(url_for('change_price', operation = operation))

    elif operation == "addcategory":
      return redirect(url_for('addcategory', operation = operation))

    elif operation == "addmanufacturer":
      return redirect(url_for('addmanufacturer', operation = operation))

    elif operation == "viewcategory":
      return redirect(url_for('view_category', operation = operation ))

    elif operation == "viewmanufacturers":
      return redirect(url_for('view_manufacturer', operation = operation ))

    else:
      #print operation
      return render_template('errorstatus.html', statusmessage =  " Select a button " , redirecturl = '/hq')

  elif request.method == "GET":
    return render_template('HQshop_related_operation.html', form = form)

@app.route('/stockgroupedbyshop/<int:page>', methods = ['GET', 'POST'])
def stock_grouped_by_shop(page = 1):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = SearchShopId()
  if request.method == "POST":

    form_validation = form.validateNotEmpty(form.shopId)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for shopid" , redirecturl = '/stockgroupedbyshop/stockgroupedbyshop')
    form_validation = form.validateNumber(form.shopId)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for shopid" , redirecturl = '/stockgroupedbyshop/stockgroupedbyshop')

    logicObject = Logic.Logic()
    storageObject = StorageClass()
    #stockobjbyshop = logicObject.execute("stockgroupedbyshop",form)
    stockobjbyshop = storageObject.get_paginate_grouped_shopId(page, POSTS_PER_PAGE, form.shopId.data)
    return render_template('listingstocks.html', allstocks = stockobjbyshop)

  elif request.method == 'GET':
    return render_template('searchshopid.html',form = form)

@app.route('/stockdisplayall/<int:page>')
def view_stock(page = 1):
  if 'email' not in session:
    return redirect(url_for('signin'))

  logicObject = Logic.Logic()
  storageObject = StorageClass()
  #allstocks = logicObject.execute(operation, None)
  allstocks = storageObject.get_paginate_stock(page,POSTS_PER_PAGE)
  return render_template('listingstocks.html', allstocks = allstocks)

@app.route('/transactiongroupedbyshop/<operation>', methods = ['GET', 'POST'])
def transaction_grouped_by_shop(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = SearchShopId()
  if request.method == "POST":

    form_validation = form.validateNotEmpty(form.shopId)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for shopid" , redirecturl = '/transactiongroupedbyshop/transactiongroupedbyshop')
    form_validation = form.validateNumber(form.shopId)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for shopid" , redirecturl = '/transactiongroupedbyshop/transactiongroupedbyshop')

    logicObject = Logic.Logic()
    #storageObject = StorageClass()
    transactionobjbyshop = logicObject.execute(operation,form)
    #transactionobjbyshop = storageObject.get_paginate_transaction_grouped_shopId(page,POSTS_PER_PAGE,form.shopId.data)
    return render_template('transactionbyshopid.html', transactionobjbyshop = transactionobjbyshop)

  elif request.method == 'GET':
    return render_template('searchshopid.html',form = form)

@app.route('/transactiondisplayall/<int:page>')
def view_all_transaction(page = 1):
  if 'email' not in session:
    return redirect(url_for('signin'))

  logicObject = Logic.Logic()
  storageObject = StorageClass()
  #alltransactions = logicObject.execute(operation, None)
  alltransactions = storageObject.get_paginate_soldstock(page,POSTS_PER_PAGE)
  return render_template('listingtransactions.html', alltransactions = alltransactions)

@app.route('/deleteproduct/<operation>', methods = ['POST', 'GET'])
def delete_product(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = SearchBarcode()
  if request.method == "POST":

    form_validation = form.validateNotEmpty(form.barcode)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/deleteproduct/deleteproduct')
    form_validation = form.validateNumber(form.barcode)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/deleteproduct/deleteproduct')

    logicObject = Logic.Logic()
    feedback = logicObject.execute(operation, form)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == 'GET':
    return render_template('deletebarcode.html',form = form)

@app.route('/updateproduct/<operation>', methods = ['POST', 'GET'])
def update_product(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = SearchBarcode()
  if request.method == "POST":

    form_validation = form.validateNotEmpty(form.barcode)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/updateproduct/updateproduct')
    form_validation = form.validateNumber(form.barcode)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/updateproduct/updateproduct')

    formbarcode = form.barcode.data
    return redirect(url_for('actual_updateproduct', formbarcode = formbarcode))

  elif request.method == 'GET':
    return render_template('searchbarcode.html', form = form)

@app.route('/toupdateproduct/<formbarcode>', methods = ['POST', 'GET'])
def actual_updateproduct(formbarcode):
  if 'email' not in session:
    return redirect(url_for('signin'))

  updateproductinfo = UpdateProductForm()
  logicObject = Logic.Logic()
  if request.method == "POST":

    form_validation = updateproductinfo.validateNotEmpty(updateproductinfo.barcode)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/updateproduct/updateproduct')
    form_validation = updateproductinfo.validateNumber(updateproductinfo.barcode)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/updateproduct/updateproduct')

    form_validation = updateproductinfo.validateNotEmpty(updateproductinfo.proname)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for name" , redirecturl = '/updateproduct/updateproduct')

    form_validation = updateproductinfo.validateNotEmpty(updateproductinfo.price)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for price" , redirecturl = '/updateproduct/updateproduct')

    form_validation = updateproductinfo.validateFloat(updateproductinfo.price)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for price" , redirecturl = '/updateproduct/updateproduct')

    form_validation = updateproductinfo.validateNotEmpty(updateproductinfo.minStock)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for minStock" , redirecturl = '/updateproduct/updateproduct')
    form_validation = updateproductinfo.validateNumber(updateproductinfo.minStock)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for minStock" , redirecturl = '/updateproduct/updateproduct')

    form_validation = updateproductinfo.validateNotEmpty(updateproductinfo.bundleUnit)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for bundleUnit" , redirecturl = '/updateproduct/updateproduct')
    form_validation = updateproductinfo.validateNumber(updateproductinfo.bundleUnit)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for bundleUnit" , redirecturl = '/updateproduct/updateproduct')

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
  if 'email' not in session:
    return redirect(url_for('signin'))

  return redirect(url_for('search_barcode', operation = operation))

@app.route('/deleteshop/<operation>', methods = ['POST', 'GET'])
def delete_shop(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = RetrieveShop()
  if request.method == "POST":

    form_validation = form.validateNotEmpty(form.shopId)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for shopid" , redirecturl = '/deleteshop/deleteshop')
    form_validation = form.validateNumber(form.shopId)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for shopid" , redirecturl = '/deleteshop/deleteshop')

    logicObject = Logic.Logic()
    feedback = logicObject.execute(operation, form)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == 'GET':
    return render_template('deleteshopid.html',form = form)

@app.route('/updateshop/<operation>', methods = ['POST','GET'])
def update_shop(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = RetrieveShop()
  if request.method == "POST":
    
    formshopid = form.shopId.data
    return redirect(url_for('check_update',formshopid = formshopid ))

  elif request.method == 'GET':
    return render_template('retrieveshopId.html',form = form)

@app.route('/tocheckupdate/<formshopid>', methods = ['POST', 'GET'])
def check_update(formshopid):
  if 'email' not in session:
    return redirect(url_for('signin'))

  updateshopinfo = UpdateShopForm()
  logicObject = Logic.Logic()
  if request.method == "POST":

    form_validation = updateshopinfo.validateNotEmpty(updateshopinfo.address)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for address" , redirecturl = '/updateshop/updateshop')
    
    form_validation = updateshopinfo.validateNotEmpty(updateshopinfo.admin)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for admin" , redirecturl = '/updateshop/updateshop')
    
    form_validation = updateshopinfo.validateNotEmpty(updateshopinfo.contactNumber)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for contactNumber" , redirecturl = '/updateshop/updateshop')
    form_validation = updateshopinfo.validateNumber(updateshopinfo.contactNumber)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for contactNumber" , redirecturl = '/updateshop/updateshop')

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
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = RetrieveShop()
  if request.method == "POST":

    form_validation = form.validateNotEmpty(form.shopId)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for shopid" , redirecturl = '/retrieveshop/retrieveshop')
    form_validation = form.validateNumber(form.shopId)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for shopid" , redirecturl = '/retrieveshop/retrieveshop')

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
  if 'email' not in session:
    return redirect(url_for('signin'))

  logicObject = Logic.Logic()
  allshops = logicObject.execute(operation, None)
  return render_template('listingshops.html', allshops = allshops)

@app.route('/location/<operation>', methods = ['POST', 'GET'])
def enterlocation(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = LocationShopForm()
  if request.method == "POST":
    
    form_validation = form.validateNotEmpty(form.city)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for city" , redirecturl = '/location/addlocation')
    
    form_validation = form.validateNotEmpty(form.country)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for country" , redirecturl = '/location/addlocation')

    form_validation = form.validateNotEmpty(form.tax)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for tax" , redirecturl = '/location/addlocation')

    form_validation = form.validateFloat(form.tax)
    if str(form_validation) == 'please enter valid price':
      return render_template('errorstatus.html', statusmessage = form_validation + " for tax" , redirecturl = '/location/addlocation')

    form_validation = form.validateNotEmpty(form.distance)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for distance" , redirecturl = '/location/addlocation')

    form_validation = form.validateFloat(form.distance)
    if str(form_validation) == 'please enter valid price':
      return render_template('errorstatus.html', statusmessage = form_validation + " for distance" , redirecturl = '/location/addlocation')

    logicObject = Logic.Logic()
    feedback = logicObject.execute(operation, form)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == "GET":
    return render_template('shoplocation.html', form = form)

@app.route('/shop/<operation>', methods = ['POST', 'GET'])
def addshop(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  logicObject = Logic.Logic()
  locationsall = logicObject.execute('viewlocation',None)
  loc_city_country = [(locationobj.city, locationobj.country) for locationobj in locationsall]
  #print loc_city_country
  location_choices_city = [(locationobj.city, locationobj.city) for locationobj in locationsall]
  location_choices_country = [(locationobj.country, locationobj.country) for locationobj in locationsall]
  location_choices_city = sorted(location_choices_city, key = itemgetter(1))
  location_choices_country = sorted(location_choices_country, key = itemgetter(1))
  
  #location_choices_city, location_choices_country = [(locationobj.city,locationobj.city),(locationobj.country,locationobj.country) for locationobj in locationsall]
  location_choices_city.append(('znone','None'))
  location_choices_country.append(('znone', 'None'))
  form = RegisterShopForm()
  form.city.choices = location_choices_city
  form.country.choices = location_choices_country
  if request.method == "POST":

    form_validation = form.validateNotEmpty(form.shopId)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for shopid" , redirecturl = '/shop/addshop')
    form_validation = form.validateNumber(form.shopId)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for shopid" , redirecturl = '/shop/addshop')
    
    form_validation = form.validateNotEmpty(form.address)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for address" , redirecturl = '/shop/addshop')
    
    form_validation = form.validateNotEmpty(form.admin)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for admin" , redirecturl = '/shop/addshop')
    
    form_validation = form.validateNotEmpty(form.contactNumber)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for contactNumber" , redirecturl = '/shop/addshop')
    form_validation = form.validateNumber(form.contactNumber)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for contactNumber" , redirecturl = '/shop/addshop')

    city_country_pair = (form.city.data,form.country.data)
    if city_country_pair in loc_city_country:
      feedback = logicObject.execute(operation, form)

    elif str(form.city.data) == "znone" or str(form.country.data) == "znone" :
      logicObject.execute("addlocation",form.emformlocation)
      form.city.data = form.emformlocation.city.data
      form.country.data = form.emformlocation.country.data
      feedback = logicObject.execute(operation, form) 
    else:
      country_city = [(locationobj.city, locationobj.country) for locationobj in locationsall if locationobj.country == str(form.country.data)]
      return render_template('feedbackregistershop.html',form = form, citycountry = country_city)
         
    
    return render_template('feedback.html', feedback = feedback)

  elif request.method == "GET":    
    return render_template('registershop.html',form = form)

@app.route('/productsearch/<operation>', methods = ['POST','GET'])
def search_barcode(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = SearchBarcode()
  if request.method == "POST":

    form_validation = form.validateNotEmpty(form.barcode)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/productsearch/retrieveproduct')
    form_validation = form.validateNumber(form.barcode)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/productsearch/retrieveproduct')

    logicObject = Logic.Logic()
    productobj = logicObject.execute(operation,form)
    if productobj:
      return render_template('productdetailsforbarcode.html', productobj = productobj)
    else:
      return redirect(url_for('defaulterror'))

  elif request.method == 'GET':
    return render_template('searchbarcode.html',form = form)

@app.route('/productdisplayall/<int:page>')
def view_all_products(page = 1):
  if 'email' not in session:
    return redirect(url_for('signin'))

  logicObject = Logic.Logic()
  storageObject = StorageClass()
  #allproducts = logicObject.execute(operation, None)
  allproducts = storageObject.get_paginate_products(page,POSTS_PER_PAGE)
  return render_template('listinginventory.html', allproducts = allproducts)

@app.route('/customer/<operation>', methods = ['POST', 'GET'])
#@login_required
def addcustomer(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = AddCustomer()
  msg = ""
  if request.method ==  "POST" :

    msg =  form.validateNotEmpty(form.customername)
    if msg == 'Cannot give empty space':
      return render_template('addcustomer.html', form = form, msg = msg)
    msg = form.validateNumber(form.handphone)
    if msg == 'please enter only numbers':
      return render_template('addcustomer.html', form = form, msg = msg)

    logicObject = Logic.Logic()
    feedback = logicObject.execute(operation,form)
    return render_template('feedback.html', feedback = feedback)
    
  elif request.method == 'GET':
    return render_template('addcustomer.html', form = form, msg = msg)


@app.route('/manufacturer/<operation>', methods = ['POST', 'GET'])
#@login_required    
def addmanufacturer(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))
  form = AddManufacturer()
  if request.method == "POST":
    
    form_validation = form.validateNotEmpty(form.manufacturerId)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for manufacturerId" , redirecturl = '/manufacturer/addmanufacturer')
    form_validation = form.validateNumber(form.manufacturerId)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for manufacturerId" , redirecturl = '/manufacturer/addmanufacturer')

    form_validation = form.validateNotEmpty(form.mname)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for manufacturer name" , redirecturl = '/manufacturer/addmanufacturer')

    logicObject = Logic.Logic()
    feedback = logicObject.execute(operation,form)
    return render_template('feedback.html',feedback = feedback)
  
  elif request.method == 'GET':
    return render_template('addmanufacturer.html', form = form) 

@app.route('/category/<operation>', methods = ['POST', 'GET'])
#@login_required
def addcategory(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = AddCategory()
  if request.method == "POST":
    
    form_validation = form.validateNotEmpty(form.categoryId)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for categoryId" , redirecturl = '/category/addcategory')
    form_validation = form.validateNumber(form.categoryId)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for categoryId" , redirecturl = '/category/addcategory')

    form_validation = form.validateNotEmpty(form.categoryDescription)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for categoryDescription" , redirecturl = '/category/addcategory')

    logicObject = Logic.Logic()
    feedback = logicObject.execute(operation,form)
    return render_template('feedback.html',feedback = feedback)
  
  elif request.method == 'GET':
    return render_template('addcategory.html', form = form) 
  
@app.route('/productadd/<operation>', methods = ['POST', 'GET'])
#@login_required    
def addproduct(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  logicObject = Logic.Logic()
  manufacturers = logicObject.execute('viewmanufacturers',None)
  manufacturer_choices = [(manufacturer.manufacturerId,manufacturer.name) for manufacturer in manufacturers]
  #manufacturer_choices.append(('-1','None'))
  categories = logicObject.execute('viewcategories',None)
  category_choices =[(category.categoryId,category.categoryDescription) for category in categories]
  #category_choices.append(('-1','None'))
  
  form = AddProduct() 
  form.manufacturerId.choices = manufacturer_choices
  form.category.choices = category_choices
  if request.method == "POST":

    form_validation = form.validateNotEmpty(form.barcode)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/productadd/addproduct')
    form_validation = form.validateNumber(form.barcode)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/productadd/addproduct')

    form_validation = form.validateNotEmpty(form.proname)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for name" , redirecturl = '/productadd/addproduct')

    form_validation = form.validateNotEmpty(form.price)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for price" , redirecturl = '/productadd/addproduct')

    form_validation = form.validateFloat(form.price)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for price" , redirecturl = '/productadd/addproduct')

    form_validation = form.validateNotEmpty(form.minStock)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for minStock" , redirecturl = '/productadd/addproduct')
    form_validation = form.validateNumber(form.minStock)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for minStock" , redirecturl = '/productadd/addproduct')

    form_validation = form.validateNotEmpty(form.cacheStockQty)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for cacheStockQty" , redirecturl = '/productadd/addproduct')
    form_validation = form.validateNumber(form.cacheStockQty)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for cacheStockQty" , redirecturl = '/productadd/addproduct')

    form_validation = form.validateNotEmpty(form.bundleUnit)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for bundleUnit" , redirecturl = '/productadd/addproduct')
    form_validation = form.validateNumber(form.bundleUnit)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for bundleUnit" , redirecturl = '/productadd/addproduct')

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
  if 'email' not in session:
    return redirect(url_for('signin'))

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
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = BuyItem()
  if request.method == 'POST':
    logicObject = Logic.Logic()
    feedback = logicObject.execute('buyitem',form)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == 'GET':
    return render_template('buyitem.html', form=form)

@app.route('/defaulterror')
def defaulterror():
  if 'email' not in session:
    return redirect(url_for('signin'))

  return render_template('errorstatus.html', statusmessage = "data not present" , redirecturl = '/hq')

#to check the database part works fine
@app.route('/db')
def db_check():
  checkdb = Check()
  return checkdb.check_id()


#to check server information
@app.route('/serverinfo', methods = ['POST']) 
def server_info():
  #print "hello"
  stock_soldstock = request.data
  all_data = json.loads(stock_soldstock)
  for key, value in all_data.items():
    shopid = key
    stock_soldstock_dict = value
  stock_info = {}
  soldstock_info = {}
  
  for key, value in stock_soldstock_dict.items():
    if key == 'Stock':
      key_stock = key
      stock_list = value
    elif key == 'SoldStock':
      key_soldstock = key
      soldstock_list = value
  
  feedback_json = {}
  if len(stock_list) == 0 and len(soldstock_list) == 0:
    feedback_json['feedback'] = "stock and soldstock empty"
    return jsonify(feedback_json)

  if len(stock_list) == 0 and len(soldstock_list)>0:
    feedback_json['feedback'] = "stock empty so soldstock not added"
    return jsonify(feedback_json)

  #stock_list = stock_soldstock_dict['Stock']
  #soldstock_list = stock_soldstock_dict['SoldStock']

  stock_form = StockForm()
  soldstock_form = SoldStockForm()
  logicObject = Logic.Logic()

  if len(stock_list) > 0:
    keys_stock_list = list(sorted(stock_list[0].viewkeys()))
  if len(soldstock_list) > 0:
    keys_soldstock_list = list(sorted(soldstock_list[0].viewkeys()))
  #print keys_stock_list
  #print keys_soldstock_list
  for i in range(len(stock_list)):
    stock_info = literal_eval(json.dumps(stock_list[i]))
    stock_form.barcode.data = stock_info[keys_stock_list[0]]
    stock_form.shopId.data = shopid
    stock_form.stockQty.data = stock_info[keys_stock_list[1]]
    feedback = logicObject.execute('addstock',stock_form)
    #print feedback.getinfo()
    #print stock_info['ShopId']
    if feedback.getcommandtype() == "FAddStock":
      #print "entering"
      feedback = logicObject.execute('updatestock',stock_form)
  
  #print soldstock_list
  #print len(soldstock_list)
  for j in range(len(soldstock_list)):
    soldstock_info = literal_eval(json.dumps(soldstock_list[j]))
    soldstock_form.barcode.data = soldstock_info[keys_soldstock_list[0]]
    soldstock_form.priceSold.data = soldstock_info[keys_soldstock_list[1]]
    soldstock_form.unitSold.data = soldstock_info[keys_soldstock_list[2]]
    soldstock_form.shopId.data = shopid
    soldstock_form.timeStamps.data = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    #print soldstock_form.timeStamps.data
    feedback = logicObject.execute('addsoldstock',soldstock_form)
    #print feedback.getinfo()
    #print feedback.getdata()
    #print feedback.getcommandtype()
  feedback_json['feedback'] = "success data received"

  return jsonify(feedback_json)

@app.route('/download', methods = ['GET'])
def allow_download():
  fname = 'newitems.txt'
  try:
    with open(fname):
      f = open(fname,"r")
      contentdata = f.read()
      list_content = contentdata.split(';')
      send_json = {'update': list_content}
      f.close()
      return jsonify(send_json)
  except IOError:
      no_file = {'update':'No file'}
      return jsonify(no_file)

@app.route('/getstock', methods = ['GET'])
def get_stock():
  form = BuyItem()
  indata = request.data
  getstock = json.loads(indata)
  logicObject = Logic.Logic()
  for key,value in getstock.items():
    list_bar_quantity = value

  to_sendlist = []
  for bar_quantity in list_bar_quantity:
    form.barcode.data = bar_quantity['barcode']
    form.quantity.data = bar_quantity['quantity']
    res = logicObject.execute('cachestockqty', form)
    bar_quan_dict = {'barcode':bar_quantity['barcode'],'quantity':res}
    to_sendlist.append(bar_quan_dict)

  print to_sendlist
  final_data = {'getstockdata':to_sendlist}
  return jsonify(final_data)



@app.route('/changeprice/<operation>', methods = ['GET', 'POST'])
def change_price(operation):
    #if 'email' not in session:
    #  return redirect(url_for('signin'))
    form = SearchShopId()  
    if request.method == 'POST': 
      logicObject = Logic.Logic()
      #if request.method == 'POST':
      #barcode_cp = form.barcode.data
      all_shops = logicObject.execute(operation, form)
      return render_template('changeprice.html', alldata = all_shops)
    elif request.method == 'GET':
      return render_template('searchshopid.html',form = form)
    #elif request.method == 'GET':
    # return render_template('changeprice.html', form = form)
#def auto_change_price():
#    global all_bar_price
#    all_bar_price = []
#    logicObject = Logic.Logic()
#    #if request.method == 'POST':
#   #barcode_cp = form.barcode.data
#    all_bar_price = logicObject.execute("changeprice", None)
#    #newprice = feedback.getdata()
#    print all_bar_price[0]
#    return all_bar_price[0]

@app.route('/getprice', methods = ['GET'])
def get_price():
  #return str(all_bar_price)
  #indata = request.data
  #dict_barcode = json.loads(indata)
  #inbarcode = dict_barcode['barcode']
  #{'barcode':barcodevalue,'newprice':newprice}

  storageObject = StorageClass()
  indata = request.data
  getshopid = json.loads(indata)
  form = SearchShopId()
  logicObject = Logic.Logic()
  form.shopId.data = getshopid['shopid']
  change_bar_price = logicObject.execute("changeprice", form)
  #shopidvalue = getshopid['shopid']
  price_bar = {'barcodeprice':change_bar_price}
  return jsonify(price_bar)

@app.route('/settings', methods = ['GET', 'POST'])
def settings():
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = SettingsForm()
  if request.method == 'POST':
    fname = "activepricefrequncy.txt"
    f = open(fname,'w')
    dataforfile = {}
    starttimeforfile = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    starttimedelta = datetime.datetime.strptime(starttimeforfile,'%Y-%m-%d %H:%M:%S' )
    endtimedelta = starttimedelta + datetime.timedelta(minutes = int(form.pricefreq.data))
    endtimeforfile = endtimedelta.strftime('%Y-%m-%d %H:%M:%S')
    dataforfile = {}
    f.write(';')
    dataforfile['activepricefreq'] = form.pricefreq.data
    f.write(str(dataforfile))
    dataforfile = {}
    f.write(';')
    dataforfile['starttime'] = starttimeforfile
    f.write(str(dataforfile))
    dataforfile = {}
    f.write(';')
    dataforfile['endtime'] = endtimeforfile
    f.write(str(dataforfile))
    f.close()
    datasent = "wriiten to file"
    return render_template('settingsfeedback.html',data = datasent)

  elif request.method == "GET":
    return render_template('settings.html', form = form)

@app.route('/viewcategory/<operation>', methods = ['GET', 'POST'])
def view_category(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  logicObject = Logic.Logic()
  categories = logicObject.execute('viewcategories',None)
  return render_template('listcategory.html', categories = categories)

@app.route('/viewmanufacturers/<operation>', methods = ['GET', 'POST'])
def view_manufacturer(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  logicObject = Logic.Logic()
  manufacturers = logicObject.execute('viewmanufacturers',None)
  return render_template('listmanufacturer.html', manufacturers = manufacturers)
