import cv2
import numpy as np
import httpx


# 1) Pre‐processing: string → (1,100,100,1) float32 array
def encode_payload_for_tf(payload: str) -> np.ndarray:
    # map to ASCII (0–127), pad/truncate to 100×100=10 000 chars
    MAXLEN = 10000
    arr = [ord(c) if ord(c) < 128 else 0 for c in payload]
    if len(arr) < MAXLEN:
        arr = arr + [0] * (MAXLEN - len(arr))
    else:
        arr = arr[:MAXLEN]
    # reshape to 100×100
    img = np.array(arr, dtype=np.float32).reshape(100, 100)
    # (optional) smooth edges via interpolation
    img = cv2.resize(img, (100, 100), interpolation=cv2.INTER_CUBIC)
    # normalize into [0,1]
    img /= 128.0
    # add batch and channel dims → shape (1,100,100,1)
    return img.reshape(1, 100, 100, 1)


# 2) Build the JSON “instances” payload
def make_tf_request_body(payload: str) -> dict:
    nd = encode_payload_for_tf(payload)
    # .tolist() makes pure Python lists of floats
    return {"signature_name": "serving_default", "instances": nd.tolist()}


def predict_xss(instance):
    tf_request = make_tf_request_body("".join(instance))
    resp = httpx.post("http://tfserving_xss:8501/v1/models/xss:predict", json=tf_request)
    data = resp.json()
    probs = data["predictions"]  # should be something like [[0.12]], [[0.98]], etc.
    print("raw probs:", probs)
    return resp
