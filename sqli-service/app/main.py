from fastapi import FastAPI
from common.models import RequestPayload, PredictionResponse
from model_utils import predict_sqli

app = FastAPI(title="SQLi-Service")


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: RequestPayload):
    scores = predict_sqli(payload.instance)
    preds = scores.json()["predictions"]
    return PredictionResponse(predictions=preds)