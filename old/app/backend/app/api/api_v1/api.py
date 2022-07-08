from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, storagetype, ping, storage, storageslot

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(storagetype.router, tags=["storageconfig"])
api_router.include_router(storage.router, tags=["storage"])
api_router.include_router(storageslot.router, tags=["storageconfig"])
api_router.include_router(ping.router, tags=["ping"] )
