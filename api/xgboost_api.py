import requests 
import json
import ast
import joblib 
from flask import Flask, request, jsonify
import traceback
import pandas as pd
import numpy as np

# defining the api-endpoint  
XGBOOST_API_ENDPOINT = "http://127.0.0.1:12345/xgboost_api"
DATABASE_API_ENDPOINT = "http://127.0.0.1:12346/database_api"
FEATURE_API_ENDPOINT = "http://127.0.0.1:12347/feature_api"

app = Flask(__name__)

### ====== reverse scale mapping ==============================

# reverse scale mapping function
def reverse_scale(prediction_scaled):
	# get real_2d from database_api
	db_response = requests.get(url = DATABASE_API_ENDPOINT + "/real_2d") 
	price_str = db_response.text
	prev_N_price = ast.literal_eval(price_str)

	# compute std and mean
	adj_price_mean, adj_price_std = np.mean(prev_N_price), np.std(prev_N_price)

	prediction = list(map(lambda x: x * adj_price_std + adj_price_mean, prediction_scaled))[0]
	return prediction

# mapping

# # post predicted price to database_api/pred_new_price: {"date": , "value": }
# print("The original prediction is:%s" % prediction)
# pred_new_price = {"date": cur_date, "value": prediction}
# database_response = requests.post(url = DATABASE_API_ENDPOINT + "/pred_new_price", json = pred_new_price) 
# print(database_response.text)
# # TODO: add 3 way handshake to make comm more stable

### ===========================================================

@app.route('/xgboost_api', methods=['POST']) # Your API endpoint URL would consist /predict
# TODO: refactor this shit to a class
def predict():
	if model:
		try:
			# print(request)
			json_ = request.json
			feature_df = pd.DataFrame(json_.items()).iloc[:, 1].to_frame().transpose()
			feature = pd.get_dummies(feature_df)
			feature.columns = model_columns
			prediction_scaled = list(model.predict(feature))

			prediction_original = reverse_scale(prediction_scaled)

			print("prediction for feature %s... is: %s" % (feature.iloc[0, :4].to_list(), prediction_original))
			return jsonify({'prediction_original': str(prediction_original)})

		except:

			return jsonify({'trace': traceback.format_exc()})
	else:
		print ('Train the model first')
		return ('No model here to use')

if __name__ == '__main__':
	try:
		port = int(sys.argv[1]) # This is for a command-line argument
	except:
		port = 12345 # If you don't provide any port then the port will be set to 12345

	model_file_name = 'xgboost_model.pkl'
	model = joblib.load(model_file_name) # Load "xgboost_model.pkl"
	print ('XGBOOST Model loaded')

	model_columns_file_name = 'xgboost_model_columns.pkl'
	model_columns = joblib.load(model_columns_file_name) # Load "xgboost_model_columns.pkl"
	print ('XGBOOST Model columns loaded')

	app.run(port=port, debug=True)