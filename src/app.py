import os
import json

from flask import Blueprint, request, jsonify

from flask_cors import CORS

from config import app, auth
from services.user import create_user
from services.product import (create_product, list_product, get_all_products_name_frag, 
    get_products_info, get_products_day, get_products_week)



blueprint = Blueprint('app', __name__, url_prefix='/tcc-api')

CORS(app)

'''----------------------------- USER -----------------------------'''
@blueprint.route('/user', methods=['POST', 'PUT'])
def create_user_route():
    response = json.dumps(request.json)
    return create_user(response)
    

@blueprint.route('/user', methods=['GET'])
@auth.login_required
def login_user_route():
    
    return auth.current_user()



'''----------------------------- PRODUCT -----------------------------'''
@blueprint.route('/product', methods=['POST', 'PUT'])
def create_product_route():
    response = json.dumps(request.json)
    return create_product(response)


@blueprint.route('/product', methods=['GET'])
def find_product_route():
    #response = json.dumps(request.args)
    return list_product()


@blueprint.route('/product/info', methods=['GET'])
def find_productInfo_route():
    return get_products_info()


@blueprint.route('/product/day', methods=['GET'])
def find_productDay_route():
    return get_products_day()


@blueprint.route('/product/week', methods=['GET'])
def find_productWeek_route():
    return get_products_week()


@blueprint.route('/product/search', methods=['GET'])
def search_product_route():
    response = request.args.get('name')
    return get_all_products_name_frag(response)


'''--------------------------------------------------------------------------------'''
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