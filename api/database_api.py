
# Database Management Service
# TODO: resolve this warning
'''
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
'''
import requests 
import json
import ast
import joblib 
from flask import Flask, request, jsonify, make_response, Response
from flask_restful import Resource, Api
import traceback
import pandas as pd
import numpy as np
import datetime
from datetime import date
from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()

# defining the api-endpoint  
XGBOOST_API_ENDPOINT = "http://127.0.0.1:12345/xgboost_api"
DATABASE_API_ENDPOINT = "http://127.0.0.1:12346/database_api"
FEATURE_API_ENDPOINT = "http://127.0.0.1:12347/feature_api"

app = Flask(__name__)
api = Api(app)

# a DB class to maintain data
class Database():
    def __init__(self):
        self.open_stock_dates = ['2019-02-08',
            '2019-02-11',
            '2019-02-12',
            '2019-02-13',
            '2019-02-14',
            '2019-02-15',
            '2019-02-19',
            '2019-02-20',
            '2019-02-21',
            '2019-02-22',
            '2019-02-25',
            '2019-02-26',
            '2019-02-27',
            '2019-02-28',
            '2019-03-01',
            '2019-03-04',
            '2019-03-05',
            '2019-03-06',
            '2019-03-07',
            '2019-03-08',
            '2019-03-11',
            '2019-03-12',
            '2019-03-13',
            '2019-03-14',
            '2019-03-15',
            '2019-03-18',
            '2019-03-19',
            '2019-03-20',
            '2019-03-21',
            '2019-03-22',
            '2019-03-25',
            '2019-03-26',
            '2019-03-27',
            '2019-03-28',
            '2019-03-29',
            '2019-04-01',
            '2019-04-02',
            '2019-04-03',
            '2019-04-04',
            '2019-04-05',
            '2019-04-08',
            '2019-04-09',
            '2019-04-10',
            '2019-04-11',
            '2019-04-12',
            '2019-04-15',
            '2019-04-16',
            '2019-04-17',
            '2019-04-18',
            '2019-04-22',
            '2019-04-23',
            '2019-04-24',
            '2019-04-25',
            '2019-04-26',
            '2019-04-29',
            '2019-04-30',
            '2019-05-01',
            '2019-05-02',
            '2019-05-03',
            '2019-05-06',
            '2019-05-07',
            '2019-05-08',
            '2019-05-09',
            '2019-05-10',
            '2019-05-13',
            '2019-05-14',
            '2019-05-15',
            '2019-05-16',
            '2019-05-17',
            '2019-05-20',
            '2019-05-21',
            '2019-05-22',
            '2019-05-23',
            '2019-05-24',
            '2019-05-28',
            '2019-05-29',
            '2019-05-30',
            '2019-05-31',
            '2019-06-03',
            '2019-06-04',
            '2019-06-05',
            '2019-06-06',
            '2019-06-07',
            '2019-06-10',
            '2019-06-11',
            '2019-06-12',
            '2019-06-13',
            '2019-06-14',
            '2019-06-17',
            '2019-06-18',
            '2019-06-19',
            '2019-06-20',
            '2019-06-21',
            '2019-06-24',
            '2019-06-25',
            '2019-06-26',
            '2019-06-27',
            '2019-06-28',
            '2019-07-01',
            '2019-07-02',
            '2019-07-03',
            '2019-07-05',
            '2019-07-08',
            '2019-07-09',
            '2019-07-10',
            '2019-07-11',
            '2019-07-12',
            '2019-07-15',
            '2019-07-16',
            '2019-07-17',
            '2019-07-18',
            '2019-07-19',
            '2019-07-22',
            '2019-07-23',
            '2019-07-24',
            '2019-07-25',
            '2019-07-26',
            '2019-07-29',
            '2019-07-30',
            '2019-07-31',
            '2019-08-01',
            '2019-08-02',
            '2019-08-05',
            '2019-08-06',
            '2019-08-07',
            '2019-08-08',
            '2019-08-09',
            '2019-08-12',
            '2019-08-13',
            '2019-08-14',
            '2019-08-15',
            '2019-08-16',
            '2019-08-19',
            '2019-08-20',
            '2019-08-21',
            '2019-08-22',
            '2019-08-23',
            '2019-08-26',
            '2019-08-27',
            '2019-08-28',
            '2019-08-29',
            '2019-08-30',
            '2019-09-03',
            '2019-09-04',
            '2019-09-05',
            '2019-09-06',
            '2019-09-09',
            '2019-09-10',
            '2019-09-11',
            '2019-09-12',
            '2019-09-13',
            '2019-09-16',
            '2019-09-17',
            '2019-09-18',
            '2019-09-19',
            '2019-09-20',
            '2019-09-23',
            '2019-09-24',
            '2019-09-25',
            '2019-09-26',
            '2019-09-27',
            '2019-09-30',
            '2019-10-01',
            '2019-10-02',
            '2019-10-03',
            '2019-10-04',
            '2019-10-07',
            '2019-10-08',
            '2019-10-09',
            '2019-10-10',
            '2019-10-11',
            '2019-10-14',
            '2019-10-15',
            '2019-10-16',
            '2019-10-17',
            '2019-10-18',
            '2019-10-21',
            '2019-10-22',
            '2019-10-23',
            '2019-10-24',
            '2019-10-25',
            '2019-10-28',
            '2019-10-29',
            '2019-10-30',
            '2019-10-31',
            '2019-11-01',
            '2019-11-04',
            '2019-11-05',
            '2019-11-06',
            '2019-11-07',
            '2019-11-08',
            '2019-11-11',
            '2019-11-12',
            '2019-11-13',
            '2019-11-14',
            '2019-11-15',
            '2019-11-18',
            '2019-11-19',
            '2019-11-20',
            '2019-11-21',
            '2019-11-22',
            '2019-11-25',
            '2019-11-26',
            '2019-11-27',
            '2019-11-29',
            '2019-12-02',
            '2019-12-03',
            '2019-12-04',
            '2019-12-05',
            '2019-12-06',
            '2019-12-09',
            '2019-12-10',
            '2019-12-11',
            '2019-12-12',
            '2019-12-13',
            '2019-12-16',
            '2019-12-17',
            '2019-12-18',
            '2019-12-19',
            '2019-12-20',
            '2019-12-23',
            '2019-12-24',
            '2019-12-26',
            '2019-12-27',
            '2019-12-30',
            '2019-12-31',
            '2020-01-02',
            '2020-01-03',
            '2020-01-06',
            '2020-01-07',
            '2020-01-08',
            '2020-01-09',
            '2020-01-10',
            '2020-01-13',
            '2020-01-14',
            '2020-01-15',
            '2020-01-16',
            '2020-01-17',
            '2020-01-21',
            '2020-01-22',
            '2020-01-23',
            '2020-01-24',
            '2020-01-27',
            '2020-01-28',
            '2020-01-29',
            '2020-01-30',
            '2020-01-31',
            '2020-02-03',
            '2020-02-04',
            '2020-02-05',
            '2020-02-06']
        self.cur_date = "2019-09-12"
        self.feature = None
        self.real_2d = [1220.170044, 1234.25]
        self.pred_new_price = None
        self.buffer_new_prices = None
        self.real_pred_150d = [{"date":"2019-02-08","value0":1095.060059,"value1":1097.4630126953},{"date":"2019-02-11","value0":1095.01001,"value1":1085.2906494141},{"date":"2019-02-12","value0":1121.369995,"value1":1104.2950439453},{"date":"2019-02-13","value0":1120.160034,"value1":1121.162109375},{"date":"2019-02-14","value0":1121.670044,"value1":1131.9459228516},{"date":"2019-02-15","value0":1113.650024,"value1":1125.4329833984},{"date":"2019-02-19","value0":1118.560059,"value1":1113.5280761719},{"date":"2019-02-20","value0":1113.800049,"value1":1131.1976318359},{"date":"2019-02-21","value0":1096.969971,"value1":1104.4798583984},{"date":"2019-02-22","value0":1110.369995,"value1":1111.8536376953},{"date":"2019-02-25","value0":1109.400024,"value1":1115.7183837891},{"date":"2019-02-26","value0":1115.130005,"value1":1119.4855957031},{"date":"2019-02-27","value0":1116.050049,"value1":1116.3596191406},{"date":"2019-02-28","value0":1119.920044,"value1":1112.7442626953},{"date":"2019-03-01","value0":1140.98999,"value1":1147.7099609375},{"date":"2019-03-04","value0":1147.800049,"value1":1134.0479736328},{"date":"2019-03-05","value0":1162.030029,"value1":1157.595703125},{"date":"2019-03-06","value0":1157.859985,"value1":1157.0297851562},{"date":"2019-03-07","value0":1143.300049,"value1":1150.6574707031},{"date":"2019-03-08","value0":1142.319946,"value1":1126.8431396484},{"date":"2019-03-11","value0":1175.76001,"value1":1153.7106933594},{"date":"2019-03-12","value0":1193.199951,"value1":1192.6280517578},{"date":"2019-03-13","value0":1193.319946,"value1":1207.703125},{"date":"2019-03-14","value0":1185.550049,"value1":1187.4252929688},{"date":"2019-03-15","value0":1184.459961,"value1":1192.6977539062},{"date":"2019-03-18","value0":1184.26001,"value1":1183.7349853516},{"date":"2019-03-19","value0":1198.849976,"value1":1191.8356933594},{"date":"2019-03-20","value0":1223.969971,"value1":1212.3620605469},{"date":"2019-03-21","value0":1231.540039,"value1":1247.5699462891},{"date":"2019-03-22","value0":1205.5,"value1":1228.4187011719},{"date":"2019-03-25","value0":1193.0,"value1":1197.6314697266},{"date":"2019-03-26","value0":1184.619995,"value1":1199.1218261719},{"date":"2019-03-27","value0":1173.02002,"value1":1181.6552734375},{"date":"2019-03-28","value0":1168.48999,"value1":1161.3210449219},{"date":"2019-03-29","value0":1173.310059,"value1":1149.5017089844},{"date":"2019-04-01","value0":1194.430054,"value1":1174.947265625},{"date":"2019-04-02","value0":1200.48999,"value1":1198.2255859375},{"date":"2019-04-03","value0":1205.920044,"value1":1188.0078125},{"date":"2019-04-04","value0":1215.0,"value1":1206.9193115234},{"date":"2019-04-05","value0":1207.150024,"value1":1210.3623046875},{"date":"2019-04-08","value0":1203.839966,"value1":1206.853515625},{"date":"2019-04-09","value0":1197.25,"value1":1199.84375},{"date":"2019-04-10","value0":1202.160034,"value1":1203.7067871094},{"date":"2019-04-11","value0":1204.619995,"value1":1192.3399658203},{"date":"2019-04-12","value0":1217.869995,"value1":1211.4743652344},{"date":"2019-04-15","value0":1221.099976,"value1":1233.8664550781},{"date":"2019-04-16","value0":1227.130005,"value1":1235.3240966797},{"date":"2019-04-17","value0":1236.339966,"value1":1248.4686279297},{"date":"2019-04-18","value0":1236.369995,"value1":1244.1759033203},{"date":"2019-04-22","value0":1248.839966,"value1":1243.0418701172},{"date":"2019-04-23","value0":1264.550049,"value1":1245.9372558594},{"date":"2019-04-24","value0":1256.0,"value1":1216.9166259766},{"date":"2019-04-25","value0":1263.449951,"value1":1226.5220947266},{"date":"2019-04-26","value0":1272.180054,"value1":1231.3063964844},{"date":"2019-04-29","value0":1287.579956,"value1":1242.1287841797},{"date":"2019-04-30","value0":1188.47998,"value1":1182.7592773438},{"date":"2019-05-01","value0":1168.079956,"value1":1194.5466308594},{"date":"2019-05-02","value0":1162.609985,"value1":1146.4895019531},{"date":"2019-05-03","value0":1185.400024,"value1":1189.28515625},{"date":"2019-05-06","value0":1189.390015,"value1":1192.7280273438},{"date":"2019-05-07","value0":1174.099976,"value1":1195.1062011719},{"date":"2019-05-08","value0":1166.27002,"value1":1169.3858642578},{"date":"2019-05-09","value0":1162.380005,"value1":1154.3283691406},{"date":"2019-05-10","value0":1164.27002,"value1":1165.4924316406},{"date":"2019-05-13","value0":1132.030029,"value1":1137.7735595703},{"date":"2019-05-14","value0":1120.439941,"value1":1117.9997558594},{"date":"2019-05-15","value0":1164.209961,"value1":1160.2333984375},{"date":"2019-05-16","value0":1178.97998,"value1":1176.1049804688},{"date":"2019-05-17","value0":1162.300049,"value1":1179.8422851562},{"date":"2019-05-20","value0":1138.849976,"value1":1132.763671875},{"date":"2019-05-21","value0":1149.630005,"value1":1135.2239990234},{"date":"2019-05-22","value0":1151.420044,"value1":1149.7481689453},{"date":"2019-05-23","value0":1140.77002,"value1":1144.1971435547},{"date":"2019-05-24","value0":1133.469971,"value1":1124.6986083984},{"date":"2019-05-28","value0":1134.150024,"value1":1121.9780273438},{"date":"2019-05-29","value0":1116.459961,"value1":1108.5234375},{"date":"2019-05-30","value0":1117.949951,"value1":1108.9659423828},{"date":"2019-05-31","value0":1103.630005,"value1":1102.9969482422},{"date":"2019-06-03","value0":1036.22998,"value1":1070.2391357422},{"date":"2019-06-04","value0":1053.050049,"value1":1054.6853027344},{"date":"2019-06-05","value0":1042.219971,"value1":1048.0482177734},{"date":"2019-06-06","value0":1044.339966,"value1":1053.3715820312},{"date":"2019-06-07","value0":1066.040039,"value1":1069.7142333984},{"date":"2019-06-10","value0":1080.380005,"value1":1076.7004394531},{"date":"2019-06-11","value0":1078.719971,"value1":1074.3411865234},{"date":"2019-06-12","value0":1077.030029,"value1":1071.7741699219},{"date":"2019-06-13","value0":1088.77002,"value1":1084.8933105469},{"date":"2019-06-14","value0":1085.349976,"value1":1083.7854003906},{"date":"2019-06-17","value0":1092.5,"value1":1085.8825683594},{"date":"2019-06-18","value0":1103.599976,"value1":1093.8271484375},{"date":"2019-06-19","value0":1102.329956,"value1":1111.3819580078},{"date":"2019-06-20","value0":1111.420044,"value1":1104.3544921875},{"date":"2019-06-21","value0":1121.880005,"value1":1119.7634277344},{"date":"2019-06-24","value0":1115.52002,"value1":1128.1947021484},{"date":"2019-06-25","value0":1086.349976,"value1":1091.0864257812},{"date":"2019-06-26","value0":1079.800049,"value1":1088.0642089844},{"date":"2019-06-27","value0":1076.01001,"value1":1073.1136474609},{"date":"2019-06-28","value0":1080.910034,"value1":1078.3419189453},{"date":"2019-07-01","value0":1097.949951,"value1":1092.1484375},{"date":"2019-07-02","value0":1111.25,"value1":1102.1529541016},{"date":"2019-07-03","value0":1121.579956,"value1":1111.43359375},{"date":"2019-07-05","value0":1131.589966,"value1":1139.8060302734},{"date":"2019-07-08","value0":1116.349976,"value1":1129.9738769531},{"date":"2019-07-09","value0":1124.829956,"value1":1111.3176269531},{"date":"2019-07-10","value0":1140.47998,"value1":1145.2125244141},{"date":"2019-07-11","value0":1144.209961,"value1":1129.8035888672},{"date":"2019-07-12","value0":1144.900024,"value1":1123.3875732422},{"date":"2019-07-15","value0":1150.339966,"value1":1134.4119873047},{"date":"2019-07-16","value0":1153.579956,"value1":1147.3579101562},{"date":"2019-07-17","value0":1146.349976,"value1":1153.2639160156},{"date":"2019-07-18","value0":1146.329956,"value1":1152.4227294922},{"date":"2019-07-19","value0":1130.099976,"value1":1129.8391113281},{"date":"2019-07-22","value0":1138.069946,"value1":1143.7293701172},{"date":"2019-07-23","value0":1146.209961,"value1":1136.6883544922},{"date":"2019-07-24","value0":1137.810059,"value1":1140.7744140625},{"date":"2019-07-25","value0":1132.119995,"value1":1129.2729492188},{"date":"2019-07-26","value0":1250.410034,"value1":1198.1995849609},{"date":"2019-07-29","value0":1239.410034,"value1":1229.1066894531},{"date":"2019-07-30","value0":1225.140015,"value1":1228.8532714844},{"date":"2019-07-31","value0":1216.680054,"value1":1228.4569091797},{"date":"2019-08-01","value0":1209.01001,"value1":1227.6983642578},{"date":"2019-08-02","value0":1193.98999,"value1":1206.2584228516},{"date":"2019-08-05","value0":1152.319946,"value1":1190.2747802734},{"date":"2019-08-06","value0":1169.949951,"value1":1172.4749755859},{"date":"2019-08-07","value0":1173.98999,"value1":1173.0751953125},{"date":"2019-08-08","value0":1204.800049,"value1":1187.8195800781},{"date":"2019-08-09","value0":1188.01001,"value1":1182.2690429688},{"date":"2019-08-12","value0":1174.709961,"value1":1202.8693847656},{"date":"2019-08-13","value0":1197.27002,"value1":1188.9157714844},{"date":"2019-08-14","value0":1164.290039,"value1":1172.9141845703},{"date":"2019-08-15","value0":1167.26001,"value1":1161.6119384766},{"date":"2019-08-16","value0":1177.599976,"value1":1159.0770263672},{"date":"2019-08-19","value0":1198.449951,"value1":1192.1213378906},{"date":"2019-08-20","value0":1182.689941,"value1":1177.3610839844},{"date":"2019-08-21","value0":1191.25,"value1":1185.4798583984},{"date":"2019-08-22","value0":1189.530029,"value1":1191.0361328125},{"date":"2019-08-23","value0":1151.290039,"value1":1167.1713867188},{"date":"2019-08-26","value0":1168.890015,"value1":1167.4237060547},{"date":"2019-08-27","value0":1167.839966,"value1":1149.9976806641},{"date":"2019-08-28","value0":1171.02002,"value1":1156.7370605469},{"date":"2019-08-29","value0":1192.849976,"value1":1183.8461914062},{"date":"2019-08-30","value0":1188.099976,"value1":1193.2807617188},{"date":"2019-09-03","value0":1168.390015,"value1":1181.1267089844},{"date":"2019-09-04","value0":1181.410034,"value1":1163.7657470703},{"date":"2019-09-05","value0":1211.380005,"value1":1199.3079833984},{"date":"2019-09-06","value0":1204.930054,"value1":1206.5615234375},{"date":"2019-09-09","value0":1204.410034,"value1":1203.2408447266},{"date":"2019-09-10","value0":1206.0,"value1":1209.3107910156},{"date":"2019-09-11","value0":1220.170044,"value1":1211.3041992188},{"date":"2019-09-12","value0":1234.25,"value1":1241.3234863281}]

db = Database()

def update_real_2d(real_2d, new_price):
    """@params:
        real_2d: List[int]
        new_price: int 
    """
    # left shift the real_2d for 1 day
    # debug
    print("===========")
    print("updating real_2d:", real_2d, " with %s" % new_price)
    print("updated real_2d will be: ", real_2d[1:] + [new_price])
    print("===========")
    return real_2d[1:] + [new_price]

def update_buffer_new_prices(buffer, real_new_price_w_date=None, pred_new_price_w_date=None):
    # TODO: now the buffer only stores 1 entry, can be modified so that it can store a queue.
    global db
    """@params:
        buffer: dict
        real_new_price_w_date: dict
        pred_new_price_w_date: dict
    """
    # take care of the parallelism of real and pred price
    # 1. buffer is None or buffer is complete -> update buffer -> don't update real_pred_150d
    # 2. buffer is half complete -> update buffer -> update real_pred_150d
    new_date = (real_new_price_w_date or pred_new_price_w_date)["date"]
    if buffer is None or (buffer["value0"] and buffer["value1"]):
        buffer = {"date": new_date, "value0": 0, "value1": 0}
        buffer["value0"], buffer["value1"] = real_new_price_w_date["value"] if real_new_price_w_date else None, pred_new_price_w_date["value"] if pred_new_price_w_date else None
        print("buffer half complete:", buffer)
    else:
        buffer["value0"], buffer["value1"] = real_new_price_w_date["value"] if real_new_price_w_date else buffer["value0"], pred_new_price_w_date["value"] if pred_new_price_w_date else buffer["value1"]
        print("buffer complete:", buffer)
        db.real_pred_150d = update_real_pred_150d(db.real_pred_150d, buffer)
        # update date only after real_pred_150d is updated
        db.cur_date = new_date
        # recover pred_new_price back to None
        db.pred_new_price = None
        # clear buffer
        buffer = None
        print("buffer cleared:", buffer)
    return buffer

def update_real_pred_150d(real_pred_150d, buffer):
    """@params:
        real_pred_150d: List[dict]
        buffer: dict: {"date": , "value0": , "value1": } 
            Note: buffer has to be complete
    """
    return real_pred_150d[1:] + [buffer]

def get_pred_new_price(feature):
    global XGBOOST_API_ENDPOINT
    # sending post request and saving response as response object 
    xgb_response = requests.post(url = XGBOOST_API_ENDPOINT, json = feature) 

    # extracting response text: scaled prediction
    # convert stringified json to listed json for scaled_prediction
    result_json = json.loads(xgb_response.text)                 # json obj          e.g.: {'prediction_scaled': '[-1.4321082]'}
    predicted_value_json = result_json['prediction_scaled']     # string of a list  e.g.: '[-1.4321082]'
    prediction_original = json.loads(predicted_value_json)      # list              e.g.: [-1.4321082]
    print("The original prediction is:%s" % prediction_original[0])     

def update_pred_new_price(pred_new_price_with_date):
    # TODO: substitute global call with thread locks
    global db
    pred_new_date = pred_new_price_with_date["date"]
    # debug
    '''print("==================================================")
    print("updating pred_new_price on date %s..., price is %s" % (pred_new_date, pred_new_price_with_date["value"]))
    print("db.cur_date is: %s" % db.cur_date)
    print("buffer is: ", db.buffer_new_prices)
    print("==================================================")'''
    if date.fromisoformat(db.cur_date) >= date.fromisoformat(pred_new_date): return "Duplicate Date"
    print(pred_new_price_with_date, db.buffer_new_prices)
    if db.buffer_new_prices and db.buffer_new_prices["value1"] != None: return "Duplicate Price"
    pred_new_price = pred_new_price_with_date["value"]
    # pred_new_price_with_date["value"] = pred_new_price
    db.pred_new_price = pred_new_price
    db.buffer_new_prices = update_buffer_new_prices(db.buffer_new_prices, None, pred_new_price_with_date)
    # debug
    '''print("==================================================")
    print("updated pred_new_price on date %s..., price is %s" % (pred_new_date, pred_new_price_with_date["value"]))
    print("db.cur_date is: %s" % db.cur_date)
    print("buffer is: ", db.buffer_new_prices)
    print("==================================================")'''
    
# implement a DBMS class
class DBMS(Resource):
    def get(self, data_name):
        global db, FEATURE_API_ENDPOINT
        # options:
        #   - feature
        #   - real_2d
        #   - real_pred_150d
        #   - pred_new_price
        #   - next_real_price
        try:
            print("GET request for " + data_name + " received", end=": ")
            if data_name == 'feature':
                print(db.feature)
                return db.feature
            elif data_name == "real_2d":
                print(db.real_2d)
                return db.real_2d
            elif data_name == "real_pred_150d":
                print(db.real_pred_150d[-1])
                return db.real_pred_150d
            elif data_name == "pred_new_price":
                print(db.pred_new_price)
                return db.pred_new_price
            elif data_name == "next_real_price":
                # increment db.cur_date until it's found in db.open_stock_dates or out of boundary
                next_date = date.fromisoformat(db.cur_date) + datetime.timedelta(1)
                while date.isoformat(next_date) not in db.open_stock_dates and next_date <= date(2020, 2, 6):
                    next_date = next_date + datetime.timedelta(1)
                if next_date > date(2020, 2, 6): return "Latest Data Not Available!"
                # request to feature_api for new features with next_date
                real_price_response = requests.post(url = FEATURE_API_ENDPOINT + '/real_new_price', json = date.isoformat(next_date)) 
                real_price_json = json.loads(real_price_response.text)
                real_price = real_price_json["value0"]
                
                # debug 
                '''print("==================================================")
                print("getting next_real_price on date %s..., price is %s" % (next_date, real_price))
                print("db.cur_date is: %s" % db.cur_date)
                print("buffer is: ", db.buffer_new_prices)
                print("==================================================")'''
                
                # update real_2d
                db.real_2d = update_real_2d(db.real_2d, real_price)
                
                # update buffer with real price
                db.buffer_new_prices = update_buffer_new_prices(db.buffer_new_prices, {"date": date.isoformat(next_date), "value": real_price}, None)
                # debug 
                '''print("==================================================")
                print("got next_real_price on date %s..., price is %s" % (next_date, real_price))
                print("db.cur_date is: %s" % db.cur_date)
                print("buffer is: ", db.buffer_new_prices)
                print("==================================================")'''
                
                return "Latest Real Price on %s Updated" % next_date.isoformat()
            else:
                print("GET requested data name: %s not found!" % data_name)
                return None
        except:
            return jsonify({'trace': traceback.format_exc()})

    def post(self, data_name):
        global db, FEATURE_API_ENDPOINT, XGBOOST_API_ENDPOINT
        # options:
        #   - feature
        #   - real_new_price (used to update real_2d and real_pred_150d)
        #   - pred_new_price
        try:
            if data_name == 'feature':
                db.feature = request.json
            elif data_name == "real_new_price":
                # TODO: deprecated 
                real_new_price_with_date = request.json
                real_new_date = real_new_price_with_date["date"]
                if date.fromisoformat(db.cur_date) >= date.fromisoformat(real_new_date): return "Duplicate Date"
                if db.buffer_new_prices and db.buffer_new_prices["value0"] != None: return "Duplicate Price"
                real_new_price = real_new_price_with_date["value"]

                # TODO: refactor, update global var inside function
                db.real_2d = update_real_2d(db.real_2d, real_new_price)
                db.buffer_new_prices = update_buffer_new_prices(db.buffer_new_prices, real_new_price_with_date, None)
                # wait until 2 new values are all updated to update real_pred_150d
            elif data_name == "pred_new_price":
                pred_new_price_with_date = request.json
                pred_new_date = pred_new_price_with_date["date"]
                if date.fromisoformat(db.cur_date) >= date.fromisoformat(pred_new_date): return "Duplicate Date"
                print(pred_new_price_with_date, db.buffer_new_prices)
                if db.buffer_new_prices and db.buffer_new_prices["value1"] != None: return "Duplicate Price"
                pred_new_price = pred_new_price_with_date["value"]
                # pred_new_price_with_date["value"] = pred_new_price
                db.pred_new_price = pred_new_price
                db.buffer_new_prices = update_buffer_new_prices(db.buffer_new_prices, None, pred_new_price_with_date)
                # db.real_pred_150d = update_real_pred_150d(db.real_pred_150d, None, pred_new_price_with_date)
            elif data_name == "next_day":
                
                # increment db.cur_date until it's found in db.open_stock_dates or out of boundary
                next_date = date.fromisoformat(db.cur_date) + datetime.timedelta(1)
                while date.isoformat(next_date) not in db.open_stock_dates and next_date <= date(2020, 2, 6):
                    next_date = next_date + datetime.timedelta(1)
                if next_date > date(2020, 2, 6): return "Latest Pred Price Not Available!"
                
                # request to feature_api for new features with next_date
                feature_response = requests.post(url = FEATURE_API_ENDPOINT + '/feature', json = date.isoformat(next_date)) 
                feature_json = json.loads(feature_response.text)
                
                # request to xgboost_api for pred_new_price with feature_json
                xgboost_response = requests.post(url = XGBOOST_API_ENDPOINT, json = feature_json)
                nested_json = json.loads(xgboost_response.text)
                pred_new_value_json = nested_json['prediction_original']
                prediction_original = json.loads(pred_new_value_json)
                print("feedback from xgb is: %s, %s" % (next_date.isoformat(), prediction_original))
                update_pred_new_price({"date": next_date.isoformat(), "value": prediction_original})
                return "Latest Pred Price on %s Updated" % next_date.isoformat()
            else:
                print("POST requested data name: %s not found!" % data_name)
                return None
        except:
            return jsonify({'trace': traceback.format_exc()})
        print(data_name + " updated: ", request.json)
        # print(db.real_pred_150d)
        return "RCV"

    # this is for CORS preflight to work
    def options(self, data_name):
        resp = Response("Test CORS")
        resp.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
        resp.headers['Access-Control-Allow-Methods'] = 'GET'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return resp

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

api.add_resource(DBMS, '/database_api/<data_name>', endpoint="database_api")

if __name__ == '__main__':
	try:
		port = int(sys.argv[1]) # This is for a command-line argument
	except:
		port = 12346 # If you don't provide any port then the port will be set to 12346

	print ('Database Management Running...')

	app.run(port=port, debug=True)