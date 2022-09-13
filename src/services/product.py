import json 

from bson import json_util, ObjectId
from flask import Response
#from werkzeug.security import generate_password_hash

from config import mongo, bd_table

db = mongo.get_database(bd_table).product

'''----------------------------CREATE PRODUCT----------------------------'''
def create_product(self):
  args = json.loads(self)
  id = args.get('_id')
  name = args.get('name')
  brand = args.get('brand')
  price = args.get('price')
  post_date = args.get('post_date')

  #if id exists, then the method is to EDIT,
  if id is not None:
    return edit_product(id, name, brand, price, post_date)

  #Find data by name ---> if finds, then the name is already been used
  product = get_product_name(name)
  if product:
    response = json_util.dumps({'message: Já existe um produto cadastrado com esse nome!!'})
    return Response(response, mimetype='aplication/json', status=409)

  #Continue with normal user creation
  id = db.insert_one(
    {'name': name, 'brand': brand, 'price': price, 'post_date': post_date}
  )
  jsonData = {
    'id': str(id.inserted_id),
    'name': name,
    'brand': brand,
    'price': price,
    'post_date': post_date
  }
  response = json_util.dumps(jsonData)
  return Response(response, mimetype='application/json', status=201)

'''----------------------------GET PRODUCT by name----------------------------'''
def get_product_name(name):
  return db.find_one({'name': name})

'''----------------------------EDIT USER----------------------------'''
def edit_product(id, name, brand, price, post_date):

  db.update_one(
    {'_id': ObjectId(id)},
    {'$set': {'name': name, 'brand': brand, 'price': price, 'post_date': post_date}}
  )
  jsonData = {
    'id': str(id),
    'name': name,
    'brand': brand,
    'price': price,
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
  return Response(response, mimetype='application/json', status=400)
