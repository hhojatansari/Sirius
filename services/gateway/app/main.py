from fastapi import FastAPI
import os
import httpx

app = FastAPI()

SERVICE_NAME = os.getenv("SERVICE_NAME", "gateway")
SERVICE_PORT = os.getenv("SERVICE_PORT", "8000")

BIOMETRIC_URL = "http://biometric:8004"
PATIENT_URL = "http://patient-registry:8002"
EHR_URL = "http://emergency-health:8003"
AUDIT_URL = "http://audit:8005"

@app.get("/")
def health():
    return {"service": SERVICE_NAME, "status": "ok", "port": SERVICE_PORT}

@app.post("/emergency/lookup")
async def lookup():
    async with httpx.AsyncClient() as client:
        bio_resp = await client.post(f"{BIOMETRIC_URL}/identify")
        candidates = bio_resp.json().get("candidates", [])
        patients = []
        for c in candidates:
            r = await client.get(f"{PATIENT_URL}/patients/{c['patient_id']}")
            patients.append(r.json())
        return {"candidates": patients}

@app.post("/emergency/confirm")
async def confirm(patient_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{EHR_URL}/patients/{patient_id}/emergency-profile")
        profile = resp.json()
        await client.post(f"{AUDIT_URL}/audit", json={"action": "emergency_lookup", "patient_id": patient_id, "user_id": "doc1"})
        return profile
