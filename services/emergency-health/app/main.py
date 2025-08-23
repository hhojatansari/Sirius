from fastapi import FastAPI
import os

app = FastAPI()

SERVICE_NAME = os.getenv("SERVICE_NAME", "emergency-health")
SERVICE_PORT = os.getenv("SERVICE_PORT", "8003")

emergency_profiles = {
    "p1": {"blood_type": "O+", "allergies": ["penicillin"], "medications": ["aspirin"]},
    "p2": {"blood_type": "A-", "allergies": [], "medications": ["metformin"]}
}

@app.get("/")
def health():
    return {"service": SERVICE_NAME, "status": "ok", "port": SERVICE_PORT}

@app.get("/patients/{patient_id}/emergency-profile")
def get_profile(patient_id: str):
    return emergency_profiles.get(patient_id, {"error": "no profile"})
