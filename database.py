from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

# SQLite DB URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./pinter5t.db"

# DB 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 세션 로컬 클래스 생성
SessionLocal = sessionmaker(
    autoflush=False, # 쿼리를 날리기 전 자동 flush X
    autocommit=False, # 명시적으로 db.commit()을 해야 함
    bind=engine
)

# Base 클래스 생성
class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session, None, None]:
    """
    DB 세션 생성 및 반환
    요청 완료 시 자동으로 세션 종료
    """

    db = SessionLocal() # 세션 생성

    try:
        yield db # 함수에 DB 세션 전달
    except:
        db.rollback()
        raise
    finally:
        db.close() # db 닫기