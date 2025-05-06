from fastapi import FastAPI
from common.models import RequestPayload, PredictionResponse
from model_utils import predict_xss

app = FastAPI(title="XSS-Service")


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: RequestPayload):
    scores = predict_xss(payload.instance)
    preds = scores.json()["predictions"]
    return PredictionResponse(predictions=preds)