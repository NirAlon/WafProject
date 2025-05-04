from __future__ import print_function
import json
import pickle
from pathlib import Path

import numpy as np
import requests
import cv2

XSS_THRESHOLD = 0.45
SQL_THRESHOLD = 0.5

# The server URL specifies the endpoint of your server running the ResNet
# model with the name "xss_model & sql_model" and using the predict interface.
SERVER_URL_XSS = 'http://localhost:8501/v1/models/xssmodel:predict'
SERVER_URL_SQL = 'http://localhost:8500/v1/models/sqlmodel:predict'

VECTORIZER_PATH = Path(__file__).parent / "vectorizer_cnn"
with open(VECTORIZER_PATH, "rb") as f:
    _vectorizer = pickle.load(f)

def make_prediction_xss(instances):
    data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(SERVER_URL_XSS, data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return predictions


def make_prediction_sql(instances):
    data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(SERVER_URL_SQL, data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return predictions


def xss_proccesor(req) -> float:
    ascii_arr = [[ord(val) for val in req]]
    img = cv2.resize(
        np.asarray(ascii_arr, dtype=np.float32),
        dsize=(100, 100),
        interpolation=cv2.INTER_CUBIC
    )
    img /= 128.0
    data = img[np.newaxis, ..., np.newaxis]
    res = make_prediction_xss(data)
    return float(res[0][0])


def predict_sqli_attack(req: str) -> float:
    features = _vectorizer.transform([req]).toarray()
    result = make_prediction_sql(features)
    return float(result[0][0])


def if_xss_text_vulnerable_without_saving_to_logger(text: str) -> bool:
    res = xss_proccesor(text)
    if res > XSS_THRESHOLD:
        return True
    else:
        return False


def if_sql_text_vulnerable_without_saving_to_logger(text: str) -> bool:
    res = predict_sqli_attack(text)
    if res > SQL_THRESHOLD:
        return True
    else:
        return False
