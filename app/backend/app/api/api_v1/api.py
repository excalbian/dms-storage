from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, storagetype

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(storagetype.router, tags=["storageconfig"])
