from fastapi import APIRouter
from app.api.routes import migrate, pre_process

api_router = APIRouter()

api_router.include_router(migrate.router, tags=["user-service"])
api_router.include_router(pre_process.router, tags=["dev-service"])
