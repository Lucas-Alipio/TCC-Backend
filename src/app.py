import os
import json

from flask import Blueprint, request, jsonify
from flask_cors import CORS

#from project
from config import app
from services.user import create_user, list_user
from services.product import create_product, list_product



blueprint = Blueprint('app', __name__, url_prefix='/tcc-api')

CORS(app)

'''----------------------------- USER -----------------------------'''
@blueprint.route('/user', methods=['POST', 'PUT'])
def create_user_route():
    response = json.dumps(request.json)
    return create_user(response)


@blueprint.route('/user', methods=['GET'])
def find_user_route():
    #response = json.dumps(request.args)
    return list_user()



'''----------------------------- PRODUCT -----------------------------'''
@blueprint.route('/product', methods=['POST', 'PUT'])
def create_product_route():
    response = json.dumps(request.json)
    return create_product(response)


@blueprint.route('/product', methods=['GET'])
def find_product_route():
    #response = json.dumps(request.args)
    return list_product()



@app.route('/')
def status():
    return jsonify({
        "message": "Back-end TCC: Aplicação rodando!!!!!!"
    })


app.register_blueprint(blueprint)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8081))
    app.run(host='0.0.0.0', port=port)


#att requirements.txt
#pip freeze > requirements.txt