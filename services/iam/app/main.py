from sqlalchemy import text
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.db import engine, get_db
from app.models import Base
from app.configs.configs import settings
from app.routers import auth, users


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.SERVICE_NAME)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/health")
def health_check():
    return {
        "service": settings.SERVICE_NAME,
        "status": "ok",
        "port": settings.SERVICE_PORT,
    }


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        print('hey.....')
        # Use connection from engine (better in SQLAlchemy 2.x)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"db": "connected"}
    except Exception as e:
        return {"db": "error", "detail": str(e)}
