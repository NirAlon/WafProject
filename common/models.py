from pydantic import BaseModel
from typing import List, Any


class RequestPayload(BaseModel):
    instance: List[Any]


class PredictionResponse(BaseModel):
    predictions: List[List[float]]
