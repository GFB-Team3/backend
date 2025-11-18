from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator

# --- common ---
class ErrorDetail(BaseModel):
    code: str
    message: str
    field: str | None = None

class ErrorResponse(BaseModel):
    detail: ErrorDetail


# --- user ---
# 회원가입 요청
class SignUpIn(BaseModel):
    email: EmailStr
    username: str
    password: str

# 로그인 요청
class LoginIn(BaseModel):
    email: EmailStr
    password: str

# 로그인 응답
class LoginOut(BaseModel):
    msg: str
    user_id: int

# 프로필 수정 요청
class UserUpdateIn(BaseModel):
    username: str

# 유저 응답
class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}  # SQLAlchemy 객체 직렬화


# --- pin ---
# class PinCreate(BaseModel):
#     pass

# class PinUpdate(BaseModel):
#     pass

class PinResponse(BaseModel):
    pin_id: int
    user_id: int
    title: str
    content: str | None = None
    image: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

