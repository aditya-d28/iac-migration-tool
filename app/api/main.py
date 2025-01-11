from fastapi import APIRouter
from app.api.routes import migrate

api_router = APIRouter()

api_router.include_router(migrate.router, tags=["user-service"])
