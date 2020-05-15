# 202005-Event-Linkage-and-Impact-Prediction
Stock Price Prediction with BERT and XGBoost using Twitter data

## Demo

### Predicted New Price on One Day

![image](https://github.com/Sapphirine/202005-Event-Linkage-and-Impact-Prediction/tree/master/demo/Predicted%20New%20Price.gif)

### Speed Up Animation

![image]https://github.com/Sapphirine/202005-Event-Linkage-and-Impact-Prediction/tree/master/demo/Stock%20Prediction%20Animation.gif)

## Prerequisites

```shell
pip install -r requirements.txt
```

## Pipeline

* Tweet Scraping
```shell
python ./twint/twitter_scraper.py
```

* Feature Extraction w./ pre-processing
	* see 1. feature_generator + sentiment.ipynb
	* download the BERT model from [here](https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-12_H-768_A-12.zip) and place it according to the directory shown in the following command.
```shell
bert-serving-start -model_dir ./model/tmp/english_L-12_H-768_A-12/ -num_worker=1
```

* Feature Aggregation
  
  * see 2. feature_aggregator + sentiment.ipynb
  
* Classification Test with price-feature
  
  * see 3. EDA_stock + XGBoost.ipynb
  
* Regression Test with all features
  
  * see 4. XGBoost for Regression.ipynb
  
## Setup for web application 

endpoints occupied:
| API        					| Port          |
| ------------- 			|:-------------:|
| feature extraction  | 12347 				|
| database      			| 12346      		|
| XGBoost 						| 12345      		|
| CORS proxy 					| 12340      		|

* under ./api folder
```shell
python feature_api.py
```
```shell
python database_api.py
```
```shell
python xgboost_api.py
```
* under ./cors-anywhere folder
```shell
node server.js
```

* open ./visualize/index/html to see the web app

# Contributing

You can [Contribute](docs/contributing.md) to this project with issues or pull requests.

# Release Notes

See [RELEASE NOTES](RELEASE_NOTES.md) file.

# License

See [MIT LICENSE](https://github.com/frostace/Event-Linkage-and-Impact-Prediction/blob/master/LICENSE) file.

# Contact

If you have any ideas, feedback, requests or bug reports, you can reach me at
[frostace0723@gmail.com](mailto:frostace0723@gmail.com)