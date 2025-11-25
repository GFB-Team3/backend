from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from routers import users as users_router
from routers import pins as pins_router
from database import Base, engine
from api import models


BASE_DIR = Path(__file__).resolve().parent              # backend/
FRONTEND_DIR = BASE_DIR.parent / "frontend" / "build"   # project-root/frontend/build


def create_app() -> FastAPI:
    app = FastAPI(
        title="pintere5t",
        version="1.0.0.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # DB 테이블 생성
    Base.metadata.create_all(bind=engine)

    # API 라우터
    app.include_router(users_router.router, prefix="/api")
    app.include_router(pins_router.router, prefix="/api")
    
    # React 정적 파일 서빙
    app.mount(
        "/src",                    
        StaticFiles(directory="src"),  
        name="src",
    )    

    @app.get("/", include_in_schema=False)
    async def index():
        return {
            "status": "ok",
            "service": "pintere5t backend",
            "docs": "/docs",
        }
    
    return app


app = create_app()