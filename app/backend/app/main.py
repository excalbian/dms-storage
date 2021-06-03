from calendar import month
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.gzip import GZipMiddleware

from authlib.jose import jwt
from app import settings
import json
from typing import Generator, List, Optional, Union, Any
from datetime import datetime, timedelta
from .core.database import get_db
from sqlalchemy.orm import Session
from .data.user import UserAccess, User
from .core.security import create_access_token

from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
from google.oauth2 import id_token
from google.auth.transport import requests

from pydantic import BaseModel, ValidationError




app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(SessionMiddleware, secret_key="some-random-string")

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"login"
)



oauth = OAuth()


CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_id = settings['GOOGLE_CLIENT_ID'],
    client_secret = settings['GOOGLE_CLIENT_SECRET'],
    client_kwargs={
        'scope': 'openid email profile'
    }
)


class Token(User):
    iss: Optional[int] = None
    sub: Optional[int] = None



@app.get('/login', tags=['authentication'])
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri,login_hint="skyspook@dallasmakerspace.org", hd='dallasmakerspace.org')

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(token, read_file('./app/jwtRS256.key.pub'))
        token_data = Token.parse_obj(payload)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(ex))
    user = token_data
    if not user or not user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return current_user

@app.get('/auth')
async def auth(request: Request):
    try:
        if request.method == 'GET' and 'code' in request.query_params:
            token = await oauth.google.authorize_access_token(request)
            user = await oauth.google.parse_id_token(request, token)
        elif request.method == 'POST':
            user = id_token.verify_oauth2_token(request.form['token'], requests.Request(), settings['GOOGLE_CLIENT_ID'])
        else:
            return HTTPException(status.HTTP_403_FORBIDDEN)
    except:
        return HTTPException(status.HTTP_403_FORBIDDEN)
    
    #user = await oauth.google.parse_id_token(request, token)
    username = user['email'].split('@')[0]
    user_access = UserAccess()
    dbuser = user_access.get_user_by_username(username)
    if dbuser is None:
        newuser = User(
            username=username, 
            email = user['email'], 
            displayname = user['name'])
        dbuser = user_access.create_user(newuser)
    access_token_expires = timedelta(minutes=int(settings['ACCESS_TOKEN_EXPIRE_MINUTES']))
    return {
        "access_token": create_access_token(
            dbuser.id,
            expires_delta=access_token_expires,
            user=dbuser
        ),
        "token_type": "bearer",
    }

@app.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)
    return RedirectResponse(url='/')

@app.get('/')
async def homepage(
    request: Request,
    user: Optional[dict] = Depends(get_current_active_user)
):
    if user is not None:
        u = json.dumps(user)
        html = (
            f'<pre>Email: {u}</pre><br>'
            '<a href="/docs">documentation</a><br>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@app.route('/openapi.json')
async def get_open_api_endpoint(
    request: Request, 
    user: Optional[dict] = Depends(get_current_active_user)  # This dependency protects our endpoint!
):
    response = JSONResponse(get_openapi(title='FastAPI', version=1, routes=app.routes))
    return response


@app.get('/docs', tags=['documentation'])  # Tag it as "documentation" for our docs
async def get_documentation(
    request: Request, 
    user: Optional[dict] = Depends(get_current_active_user)  # This dependency protects our endpoint!
):
    response = get_swagger_ui_html(openapi_url='/openapi.json', title='Documentation')
    return response