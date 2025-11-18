from datetime import datetime
from sqlalchemy import String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


# SQLAlchemy Model
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int]            = mapped_column(Integer,        primary_key=True, index=True)
    email: Mapped[str]              = mapped_column(String(255),    unique=True, index=True, nullable=False)
    password_hash: Mapped[str]      = mapped_column(String(255),    nullable=False)
    name: Mapped[str]               = mapped_column(String(50),     unique=True, nullable=False)
    username: Mapped[str]           = mapped_column(String(50),     unique=True, nullable=False)
    image: Mapped[str]
    refresh_token: Mapped[str]
    created_at: Mapped[datetime]    = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime]    = mapped_column(DateTime(timezone=True), server_default=func.now())

class Pin(Base):
    __tablename__ = "pins"

    pin_id: Mapped[int]             = mapped_column(Integer,        primary_key=True, index=True)
    user_id: Mapped[int]            = mapped_column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"))
    title: Mapped[str]              = mapped_column(String(255),    nullable=False)
    content: Mapped[str]            = mapped_column(String(255))
    image: Mapped[str]              = mapped_column(String(255),    nullable=False)
    created_at: Mapped[datetime]    = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime]    = mapped_column(DateTime(timezone=True), server_default=func.now())
