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

# Pin 생성 요청
class PinCreate(BaseModel):
     user_id: int
     title: str
     content: str
     image: str | None = None

# Pin 업데이트
class PinUpdate(BaseModel):
    user_id: int
    title: str | None = None
    content: str | None = None
    image: str | None = None

# Pin 삭제
class PinDelete(BaseModel):
    user_id: int
    

# Pin 조회 응답
class PinResponse(BaseModel):
    pin_id: int
    user_id: int
    title: str
    content: str 
    image: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- like ---

# 즐겨찾기 요청용 (요청 바디/내부 DTO)
class LikeIn(BaseModel):
    user_id: int


# 즐겨찾기 응답용 (response_model)
class LikeOut(BaseModel):
    like_id: int
    user_id: int
    pin_id: int
    created_at: datetime
    updated_at: datetime



# --- comment ---

# 댓글 등록
class CommentCreate(BaseModel):
    user_id: int
    content: str

# 댓글 수정
class CommentUpdate(BaseModel):
    user_id: int
    content: str

# 댓글 삭제
class CommentDelete(BaseModel):
    user_id: int


# 댓글 불러오기
class CommentResponse(BaseModel):
    comment_id: int
    user_id: int
    pin_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
