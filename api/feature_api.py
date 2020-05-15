
# Feature Extraction Service + Scraping Service
# TODO: resolve this warning
'''
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
'''

import joblib 
import json
from flask import Flask, request, jsonify, make_response, Response
from flask_restful import Resource, Api
import traceback
import pandas as pd
import numpy as np
from datetime import date
from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()

app = Flask(__name__)
api = Api(app)

# a Feature class to maintain data
class Feature():
    def __init__(self):
        f = open('../json/all_feature.json',) 
        # access feature like this: ft._all_feature["2019-03-04"]
        self._all_feature = json.load(f)
        g = open('../json/real_price.json',)
        self.real_new_price = json.load(g)

ft = Feature()

# implement a Feature_Extraction class
class Feature_Extraction(Resource):
    def post(self, data_name):
        global ft
        # options:
        #   - feature
        #   - real_new_price
        requested_date = request.json
        try:
            print("received POST request for %s on date: %s" % (data_name, requested_date), end=": ")
            if data_name == 'feature':
                if requested_date not in ft._all_feature: 
                    return "Not Ready!"
                print(ft._all_feature[requested_date]["adj_close_lag_1"])
                return ft._all_feature[requested_date]
            elif data_name == "real_new_price":
                if requested_date not in ft.real_new_price: 
                    return "Not Ready!"
                print(ft.real_new_price[requested_date])
                return ft.real_new_price[requested_date]
            else:
                print("data name not found!")
                return None
        except:
            return jsonify({'trace': traceback.format_exc()})

    # this is for CORS preflight to work
    def options(self, data_name):
        resp = Response("Test CORS")
        resp.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
        resp.headers['Access-Control-Allow-Methods'] = 'POST'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return resp

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

api.add_resource(Feature_Extraction, '/feature_api/<data_name>', endpoint="database_api")

if __name__ == '__main__':
	try:
		port = int(sys.argv[1]) # This is for a command-line argument
	except:
		port = 12347 # If you don't provide any port then the port will be set to 12347

	print ('Feature Extraction Service Running...')

	app.run(port=port, debug=True)