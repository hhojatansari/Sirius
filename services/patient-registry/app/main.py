from fastapi import FastAPI
import os

app = FastAPI()

SERVICE_NAME = os.getenv("SERVICE_NAME", "patient-registry")
SERVICE_PORT = os.getenv("SERVICE_PORT", "8002")

patients = {
    "p1": {"id": "p1", "name": "Alice", "dob": "1980-01-01"},
    "p2": {"id": "p2", "name": "Bob", "dob": "1975-05-05"}
}

@app.get("/")
def health():
    return {"service": SERVICE_NAME, "status": "ok", "port": SERVICE_PORT}

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    return patients.get(patient_id, {"error": "not found"})
