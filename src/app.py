import os
import json

from flask import Flask, Blueprint, request, jsonify
from flask_pymongo import MongoClient
from flask_cors import CORS

from dotenv import load_dotenv


#config
load_dotenv()

app = Flask(__name__)
app.env = os.getenv('ENV')

mongo = MongoClient('mongodb+srv://adm:adm@cluster0.oo7i1.mongodb.net/')

bd_table = app.env
#config

#app
blueprint = Blueprint('app', __name__, url_prefix='/tcc-api')

CORS(app)

#USER
@blueprint.route('/user', methods=['POST', 'PUT'])
def create_user_route():
    response = json.dumps(request.json)
    return create_user(response)


@blueprint.route('/user', methods=['GET'])
def find_user_route():
    response = json.dumps(request.args)
    return find_user(response)


#att requirements.txt
#pip freeze > requirements.txt