import json
import pandas as pd
import datetime as dt

from bson import json_util, ObjectId
from flask import Response

from config import mongo, bd_table

db = mongo.get_database(bd_table).product

'''----------------------------CREATE PRODUCT----------------------------'''
def create_product(self):
  args = json.loads(self)

  id = args.get('_id')
  name = args.get('name')
  brand = args.get('brand')
  price = args.get('price')
  address = args.get('address')
  post_date = args.get('post_date')

  #if id exists, then the method is to EDIT,
  if id is not None:
    return edit_product(id, name, brand, price, address, post_date)

  #Continue with normal product creation
  id = db.insert_one(
    {'name': name, 'brand': brand, 'price': price, 'address': address, 'post_date': post_date}
  )
  jsonData = {
    'id': str(id.inserted_id),
    'name': name,
    'brand': brand,
    'price': price,
    'address': address,
    'post_date': post_date
  }
  response = json_util.dumps(jsonData)
  return Response(response, mimetype='application/json', status=201)

'''----------------------------GET PRODUCT by name----------------------------
def get_product_name(name):
  products = db.find_one({"name": str(name)})
  response = json_util.dumps(products)
  return Response(response, mimetype='application/json', status=200)'''

'''----------------------------GET/SEARCH PRODUCT by name's fragment----------------------------'''
def get_all_products_name_frag(fragName):

  fragName = fragName.lower()
  data = json_util.dumps(db.find({}))

  #dataFrame from pandas -> dfData[c][r] ... c=column r=row
  #each row is a product , and the columns are the different types of data that each product has
  dfData = pd.read_json(data)

  searchFrag1 = dfData[dfData['name'].str.lower().str.startswith(fragName) == True]
  searchFrag2 = dfData[dfData['name'].str.lower().str.contains(fragName) == True]

  searchFrag = pd.concat([searchFrag1, searchFrag2])
  searchFrag = searchFrag.to_json(orient='records')
  
  #if finds product, then status 200-OK
  if searchFrag:
    response = searchFrag
    return Response(response, mimetype='application/json', status=200)
  
  #if not find, then status 404-not found
  response = json_util.dumps({'message': 'Nenhum registro encontrado'})
  return Response(response, mimetype='application/json', status=404)
  

'''----------------------------GET PRODUCTS DAY----------------------------'''
def get_products_day():
  
  #getting data from mongoDB
  data = json_util.dumps(db.find({}))

  #getting current date
  currentDate = dt.datetime.now() - dt.timedelta(hours=3)
  stringCurrentDate1 = currentDate.strftime("%d/%m/%y")
  stringCurrentDate2 = currentDate.strftime("%d/%m/%Y")

  #dataFrame from pandas -> dfData[c][r] ... c=column r=row
  #each row is a product , and the columns are the different types of data that each product has
  dfData = pd.read_json(data)

  #getting all products within that day
  withinADay1 = dfData[dfData['post_date'] == stringCurrentDate1]
  withinADay2 = dfData[dfData['post_date'] == stringCurrentDate2]

  withinADay = pd.concat([withinADay1, withinADay2])

  withinADay = withinADay.to_json(orient='records')

  #if finds product, then status 200-OK
  if withinADay:
    response = withinADay
    return Response(response, mimetype='application/json', status=200)
  
  #if not find, then status 404-not found
  response = json_util.dumps({'message': 'Nenhum registro encontrado'})
  return Response(response, mimetype='application/json', status=404)


'''----------------------------GET PRODUCTS WEEK----------------------------'''
def get_products_week():
  
  #getting data from mongoDB
  data = json_util.dumps(db.find({}))

  #getting current date
  currentDate = dt.datetime.now() - dt.timedelta(hours=3)
  stringCurrentDate = currentDate.strftime("%d/%m/%y")
  currentDate = dt.datetime.strptime(stringCurrentDate, "%d/%m/%y")

  #dataFrame from pandas -> dfData[c][r] ... c=column r=row
  #each row is a product , and the columns are the different types of data that each product has
  dfData = pd.read_json(data)

  #getting products within that week
  dfData['post_date'] = pd.to_datetime(dfData['post_date'], format="%d/%m/%y", errors='coerce') \
  .fillna(pd.to_datetime(dfData['post_date'], format="%d/%m/%Y", errors='coerce'))
  dfData = dfData[
    currentDate - dfData['post_date'] <= dt.timedelta(7)
  ]
  
  withinAWeek = pd.DataFrame(dfData)
  withinAWeek['post_date'] = withinAWeek['post_date'].dt.strftime("%d/%m/%y")
  withinAWeek = withinAWeek.to_json(orient='records')

  #if finds product, then status 200-OK
  if withinAWeek:
    response = withinAWeek
    return Response(response, mimetype='application/json', status=200)
  
  #if not find, then status 404-not found
  response = json_util.dumps({'message': 'Nenhum registro encontrado'})
  return Response(response, mimetype='application/json', status=404)


'''----------------------------GET PRODUCTS INFO----------------------------'''
def get_products_info():

  #getting data from mongoDB
  data = json_util.dumps(db.find({}))

  #getting current date
  currentDate = dt.datetime.now() - dt.timedelta(hours=3)
  stringCurrentDate1 = currentDate.strftime("%d/%m/%y")
  stringCurrentDate2 = currentDate.strftime("%d/%m/%Y")
  currentDate = dt.datetime.strptime(stringCurrentDate1, "%d/%m/%y")
  

  #dataFrame from pandas -> dfData[c][r] ... c=column r=row
  #each row is a product , and the columns are the different types of data that each product has
  dfData = pd.read_json(data)

  #couting the amount of products 
  total = dfData['post_date'].count()

  #counting the products within that day
  withinADay1 = dfData[dfData['post_date'] == stringCurrentDate1]
  withinADay2 = dfData[dfData['post_date'] == stringCurrentDate2]

  withinADay = pd.concat([withinADay1, withinADay2])

  withinADay = withinADay['post_date'].count()
  
  #getting products within that week
  #converting string to date
  dfData['post_date'] = pd.to_datetime(dfData['post_date'], format="%d/%m/%y", errors='coerce') \
  .fillna(pd.to_datetime(dfData['post_date'], format="%d/%m/%Y", errors='coerce'))
  dfData = dfData[
    currentDate - dfData['post_date'] <= dt.timedelta(7)
  ]
  
  withinAWeek = pd.DataFrame(dfData)

  withinAWeek = withinAWeek['name'].count()
  
  #if there is any products, then
  if data:
    response = json_util.dumps({
      'today': str(withinADay), 
      'week': str(withinAWeek), 
      'total': str(total)
    })
    return Response(response, mimetype='application/json', status=200)

  #if there isn't, then status 404-not found
  response = json_util.dumps({'message': 'Nenhum registro encontrado'})
  return Response(response, mimetype='application/json', status=404)

'''----------------------------EDIT Product----------------------------'''
def edit_product(id, name, brand, price, address, post_date):

  db.update_one(
    {'_id': ObjectId(id)},
    {'$set': {'name': name, 'brand': brand, 'price': price, 'address':address, 'post_date': post_date}}
  )
  jsonData = {
    'id': str(id),
    'name': name,
    'brand': brand,
    'price': price,
    'address': address,
    'post_date': post_date
  }
  response = json_util.dumps(jsonData)
  return Response(response, mimetype='application/json', status=202)


'''----------------------------LIST ALL PRODUCTS----------------------------'''
def list_product():

  find = db.find({})
  if find:
    response = json_util.dumps(find)
    return Response(response, mimetype='application/json', status=200)

  response = json_util.dumps({'message': 'Nenhum registro encontrado'})
  return Response(response, mimetype='application/json', status=404)
