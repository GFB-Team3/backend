from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from api.models import User

router = APIRouter(prefix="/users", tags=["users"])


# Pydantic Schemas
class SignUpIn(BaseModel):
    email: EmailStr
    username: str
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}  # SQLAlchemy 객체 직렬화


# Password Utils
from passlib.context import CryptContext
_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _hash_password(pw: str) -> str:
    return _pwd.hash(pw)

def _verify_password(pw: str, hashed: str) -> bool:
    return _pwd.verify(pw, hashed)


# Routes
@router.post("/signup", response_model=UserOut, status_code=201)
async def signup(payload: SignUpIn, db: Session = Depends(get_db)):
    # 이메일/닉네임 중복 확인
    exists = db.execute(
        select(User).where((User.email == payload.email) | (User.username == payload.username))
    ).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Email or username already exists")

    user = User(
        email=payload.email,
        username=payload.username,
        password_hash=_hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
async def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if not user or not _verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 여기서는 JWT 대신 간단한 응답만. (JWT 필요하면 알려주세요)
    return {"message": "login ok", "user_id": user.user_id}


@router.get("/{user_id}", response_model=UserOut)
async def profile(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}/pins")
async def get_my_pins(user_id: int):
    # TODO: Pin 모델/관계 설정 후 구현
    # ex) select * from pins where owner_id = :user_id
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/{user_id}", response_model=UserOut)
async def update_profile(user_id: int, payload: dict, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 간단 예시: username만 수정 허용 (원하는 필드로 확장)
    if "username" in payload:
        user.username = str(payload["username"])
    db.commit()
    db.refresh(user)
    return user
