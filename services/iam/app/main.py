from fastapi import FastAPI
import os

app = FastAPI()

SERVICE_NAME = os.getenv("SERVICE_NAME", "iam")
SERVICE_PORT = os.getenv("SERVICE_PORT", "8001")

@app.get("/")
def health():
    return {"service": SERVICE_NAME, "status": "ok", "port": SERVICE_PORT}

@app.post("/auth/login")
def login(username: str, password: str):
    return {"token": "fake-jwt-token-for-" + username}
