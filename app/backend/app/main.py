from app.api.deps import get_current_active_user
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.gzip import GZipMiddleware

from app.core.settings import settings
from app.api.api_v1.api import api_router
import json
from typing import Optional
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(GZipMiddleware, minimum_size=1000)

# # Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get('/')
async def homepage(
    request: Request,
    user: Optional[dict] = Depends(get_current_active_user)
):
    if user is not None:
        
        html = (
            f'<pre>Email: {user.email}</pre><br>'
            '<a href="/docs">documentation</a><br>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')
