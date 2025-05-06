import cv2
import numpy as np
import httpx


def predict_xss(instance):
    ascii_arr = [[ord(val) for val in "".join(instance)]]
    img = cv2.resize(
        np.asarray(ascii_arr, dtype=np.float32),
        dsize=(100, 100),
        interpolation=cv2.INTER_CUBIC
    )
    img /= 128.0
    ndarr = img[np.newaxis, ..., np.newaxis]
    tf_request = {"signature_name": "serving_default", "instances": ndarr.tolist()}
    resp = httpx.post("http://tfserving_xss:8501/v1/models/xss:predict", json=tf_request)
    return resp
