from datetime import datetime, date
from sqlalchemy import String, Integer, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


# SQLAlchemy Model
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True) # 인덱스
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False) # 이메일
    password_hash: Mapped[str]  = mapped_column(String(255), nullable=False) # 해시처리된 비밀번호
    #user_birth: Mapped[date | None] = mapped_column() # 생년월일
    username: Mapped[str]  = mapped_column(String(50), nullable=False) # 닉네임
    #gender: Mapped[int | None] = mapped_column(Integer) # 성별(0: 남자, 1: 여자: Null: 기타)
    #region: Mapped[str | None] = mapped_column(String(50)) # 국가/지역
    #language: Mapped[str | None] = mapped_column(String(50)) # 언어
    #first_name: Mapped[str | None] = mapped_column(String(50)) # 이름
    #last_name: Mapped[str | None] = mapped_column(String(50)) # 성
    #describe: Mapped[str | None] = mapped_column(String(255)) # 설명
    #website: Mapped[str | None] = mapped_column(String(255)) # 웹사이트 링크
    #image: Mapped[str | None] = mapped_column(String(255)) # 이미지 주소
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now()) # 생성일
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) # 변경일

class Pin(Base):
    __tablename__ = "pins"

    pin_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text)
    image: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Like(Base):
    __tablename__ = "likes"

    like_id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"))
    pin_id: Mapped[int] = mapped_column(Integer, ForeignKey('pins.pin_id', ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Comment(Base):
    __tablename__ = "comments"

    comment_id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    user_id: Mapped[int] = mapped_column(Integer,  ForeignKey('users.user_id', ondelete='CASCADE'))
    pin_id: Mapped[int] = mapped_column(Integer, ForeignKey('pins.pin_id', ondelete='CASCADE'))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone = True), server_default = func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())