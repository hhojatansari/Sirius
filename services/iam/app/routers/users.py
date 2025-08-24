from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.db import get_db
from app.models import User, UserRole
from app.utils.security import hash_password, decode_token
from app.configs.configs import settings

router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.post("/", status_code=201)
def create_user(
    username: str,
    password: str,
    role: UserRole = UserRole.doctor,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != UserRole.admin.value:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    exists = db.query(User).filter(User.username == username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(
        username=username,
        password=hash_password(password),
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": str(new_user.id), "username": new_user.username, "role": new_user.role.value}

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {"id": current_user["sub"], "role": current_user["role"]}
