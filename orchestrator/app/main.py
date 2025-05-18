from fastapi import FastAPI, HTTPException
from common.models import RequestPayload
import httpx

app = FastAPI(title="WAF-Orchestrator")


@app.post("/sql_api")
async def sql_api(payload: RequestPayload):
    async with httpx.AsyncClient() as client:
        body = payload.model_dump()
        resp = await client.post("http://sqli-service:8001/predict", json=body)
        preds = resp.json()["predictions"]
        print("SQLi service returned:", preds)
        score = preds[0][0]
        if score > 0.98:
            return {"allowed": False, "score": score}
        return {"allowed": True, "score": score}

@app.post("/xss_api")
async def xss_api(payload: RequestPayload):
    async with httpx.AsyncClient() as client:
        body = payload.model_dump()
        resp = await client.post("http://xss-service:8002/predict", json=body)
        data = resp.json()
        print("XSS service returned:", data)
        preds = resp.json()["predictions"]
        score = preds[0][0]
        if score > 0.05:
            return {"allowed": False, "score": score}
        return {"allowed": True, "score": score}
