from fastapi import APIRouter
from app.api.routes import ocr, system

api_router = APIRouter()

api_router.include_router(system.router, tags=["system"])
api_router.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
