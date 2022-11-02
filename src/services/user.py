import json 

from bson import json_util, ObjectId
from flask import Response

from werkzeug.security import generate_password_hash, check_password_hash

from config import mongo, bd_table, auth


db = mongo.get_database(bd_table).user

'''----------------------------CREATE USER----------------------------'''
def create_user(self):
  args = json.loads(self)
  id = args.get('_id')
  name = args.get('name')
  last_name = args.get('last_name')
  email = args.get('email')
  passw = args.get('password')

  #if id exists, then the method is to EDIT,
  if id is not None:
    return edit_user(id, name, last_name, email, passw)

  #Find data by email ---> if finds, then the email is already been used
  user = get_user_email(email)
  if user:
    response = json_util.dumps({'message: Já existe um usuário cadastrado com esse email!!'})
    return Response(response, mimetype='aplication/json', status=409)

  #Continue with normal user creation
  hash_password = generate_password_hash(passw)
  id = db.insert_one(
    {'name': name, 'last_name': last_name, 'email': email, 'password': hash_password}
  )
  jsonData = {
    'id': str(id.inserted_id),
    'name': name,
    'last_name': last_name,
    'email': email,
    'password': hash_password
  }
  response = json_util.dumps(jsonData)
  return Response(response, mimetype='application/json', status=201)

'''----------------------------GET USER by email----------------------------'''
def get_user_email(email):
  return db.find_one({'email': email})

'''----------------------------EDIT USER----------------------------'''
def edit_user(id, name, last_name, email, passw):

  #if it has a password parameter, then....
  if passw is not None:
    hash_password = generate_password_hash(passw)
    db.update_one(
      {'_id': ObjectId(id)},
      {'$set': {'name': name, 'last_name': last_name, 'email': email, 'password': hash_password}}
    )
    jsonData = {
      'id': str(id),
      'name': name,
      'last_name': last_name,
      'email': email,
    }
    response = json_util.dumps(jsonData)
    return Response(response, mimetype='application/json', status=202)
  
  #if it doesnt have a password parameter....
  db.update_one(
    {'_id': ObjectId(id)},
    {'$set': {'name': name, 'last_name': last_name, 'email': email}}
  )
  jsonData = {
    'id': str(id),
    'name': name,
    'last_name': last_name,
    'email': email,
  }
  response = json_util.dumps(jsonData)
  return Response(response, mimetype='application/json', status=202)

'''----------------------------Authentication USER----------------------------'''
@auth.verify_password
def verify_user(email, passw):

  user = get_user_email(email)
  print('user::::::::::', user)
  if not user:
    response = json_util.dumps({'message': 'Nenhum usuario com este email encontrado'})
    return Response(response, mimetype='application/json', status=400)

  if check_password_hash(user.get('password'), passw):
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json', status=202)
  
  else:
    response = json_util.dumps({'message': 'Senha digitada incorretamente'})
    return Response(response, mimetype='application/json', status=401)



'''----------------------------LIST ALL USERS----------------------------'''
def list_user():

  find = db.find({}, {'password':0})
  if find:
    response = json_util.dumps(find)
    return Response(response, mimetype='application/json', status=200)

  response = json_util.dumps({'message': 'Nenhum registro encontrado'})
  return Response(response, mimetype='application/json', status=400)

