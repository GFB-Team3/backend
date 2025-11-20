from fastapi import FastAPI

from routers import users as users_router
from routers import pins as pins_router
from database import Base, engine
from api import models 


def create_app() -> FastAPI:
    app = FastAPI(
        title="pintere5t",
        version="1.0.0.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    Base.metadata.create_all(bind=engine)
    app.include_router(users_router.router, prefix="/api")
    app.include_router(pins_router.router, prefix="/api")

    @app.get("/", include_in_schema=False)
    async def index():
        return {
            "status": "ok",
            "service": "pintere5t backend",
            "docs": "/docs",
        }
    
    return app

app = create_app()