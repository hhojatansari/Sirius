from fastapi import FastAPI
import os
from datetime import datetime

app = FastAPI()

SERVICE_NAME = os.getenv("SERVICE_NAME", "audit")
SERVICE_PORT = os.getenv("SERVICE_PORT", "8005")

logs = []

@app.get("/")
def health():
    return {"service": SERVICE_NAME, "status": "ok", "port": SERVICE_PORT}

@app.post("/audit")
def log_event(action: str, patient_id: str, user_id: str):
    event = {"action": action, "patient_id": patient_id, "user_id": user_id, "time": datetime.utcnow().isoformat()}
    logs.append(event)
    return {"saved": True, "event": event}

@app.get("/audit")
def get_logs():
    return logs
