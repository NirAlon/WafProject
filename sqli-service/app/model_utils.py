import pickle
import httpx

_vac = pickle.load(open("vectorizer_cnn.pkl", "rb"))


def predict_sqli(instance):
    X = _vac.transform(instance).toarray()
    tf_request = {"signature_name": "serving_default", "instances": X.tolist()}
    resp = httpx.post("http://tfserving_sql:8501/v1/models/sql:predict", json=tf_request)
    return resp
