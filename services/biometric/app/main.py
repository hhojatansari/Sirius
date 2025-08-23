from fastapi import FastAPI
import os

app = FastAPI()

SERVICE_NAME = os.getenv("SERVICE_NAME", "biometric")
SERVICE_PORT = os.getenv("SERVICE_PORT", "8004")

@app.get("/")
def health():
    return {"service": SERVICE_NAME, "status": "ok", "port": SERVICE_PORT}

@app.post("/identify")
def identify(modality: str = "fingerprint", payload: str = "dummy"):
    return {
        "candidates": [
            {"patient_id": "p1", "score": 0.95},
            {"patient_id": "p2", "score": 0.90}
        ]
    }
