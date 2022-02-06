from distutils.log import debug
from flask import Flask, jsonify, request
import json
from functions import allproducts,limitedProducts

app = Flask(__name__)

@app.route('/mercadolibre', methods=["GET"])
def mercadolibre():
    data = json.loads(request.data)
    if 'limit' not in data:
        title_list, images_url_list, url_list, prices_list = allproducts(data['product'])
    else:
         title_list, images_url_list, url_list, prices_list = limitedProducts(data['product'], data['limit'])
    return return Response(headers={'Access-Control-Allow-Origin':'*'}), jsonify({"datos":{"titulo":title_list, "img": images_url_list, "url":url_list, "precios": prices_list}})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)