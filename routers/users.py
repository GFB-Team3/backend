from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from api.models import User, Pin, Like
import schemas


router = APIRouter(prefix="/users", tags=["users"])


# --- Password Utils ---
#from passlib.context import CryptContext
#_pwd = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
from passlib.context import CryptContext

# bcrypt 대신 pbkdf2_sha256 사용
_pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto",
)
# 해시
def _hash_password(pw: str) -> str:
    return _pwd.hash(pw)

# 검증
def _verify_password(pw: str, hashed: str) -> bool:
    return _pwd.verify(pw, hashed)


# --- Routes --- 
# 회원가입
@router.post("/signup", response_model=schemas.UserOut, status_code=201)
async def signup(payload: schemas.SignUpIn, db: Session = Depends(get_db)):
    # 이메일 중복 확인
    # 유효성 검사 생략
    exists = db.execute(
        select(User).where((User.email == payload.email))
    ).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Email already exists")

    user = User(
        email = payload.email,
        password_hash = _hash_password(payload.password),
        username = payload.username,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

# 로그인
# todo: jwt 도입
@router.post("/login")
async def login(payload: schemas.LoginIn, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if not user or not _verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "login ok", "user_id": user.user_id}

# 프로필 조회
# todo: 인증 + 권한 체크 e.g. 나 자신 or 공개 프로필만
@router.get("/{user_id}", response_model=schemas.UserOut)
async def profile(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# 핀 목록
# todo: Pin 모델/관계 설정 후 구현
@router.get("/{user_id}/pins")
async def get_my_pins(user_id: int, db: Session = Depends(get_db)):
    pins = db.execute(
        select(Pin).where(Pin.user_id == user_id)
    ).scalars().all()

    return pins

# 프로필 수정
# todo: 권한 체크
@router.put("/{user_id}", response_model=schemas.UserOut)
async def update_profile(user_id: int, payload: schemas.UserUpdateIn, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "username" in update_data:
        user.username = update_data["username"]

    db.commit()
    db.refresh(user)

    return user


# 즐겨찾기한 핀 보기
@router.get("/{user_id}/likes", response_model=list[schemas.PinResponse])
async def get_likes(
    user_id: int,
    db: Session = Depends(get_db)
):
    
    likes = db.query(Like).filter(Like.user_id == user_id).all()

    if not likes:
        return []
    
    pin_ids = [like.pin_id for like in likes]

    pins = db.query(Pin).filter(Pin.pin_id.in_(pin_ids)).all()

    return pins