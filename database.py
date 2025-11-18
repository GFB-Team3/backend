from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./pinter5t.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autoflush=False, # 쿼리를 날리기 전 자동 flush X
    autocommit=False, # 명시적으로 db.commit()을 해야 함
    bind=engine
)

class Base(DeclarativeBase):
    """모든 ORM 모델이 상속할 기본 Base 클래스"""
    pass

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal() # 세션 생성
    try:
        yield db # 함수에 DB 세션 전달
    except:
        db.rollback()
        raise
    finally:
        db.close() # db 닫기