from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

import json
from typing import List, Optional
from app.database import SessionLocal, engine

from app.models.user import User, UserCreate, Crud as UserCrud
from app.models.permissions import PermissionCrud, PermissionsRead

from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse

from authlib.integrations.starlette_client import OAuth, OAuthError

from pydantic import BaseModel, ValidationError

config = Config('.env')

app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(SessionMiddleware, secret_key=config.file_values['MIDDLEWARE_SECRET'])


oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.get('/login', tags=['authentication'])
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    print(redirect_uri)
    print(oauth.google)
    return await oauth.google.authorize_redirect(request, redirect_uri, login_hint="skyspook@dallasmakerspace.org", hd='dallasmakerspace.org')

@app.route('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = await oauth.google.parse_id_token(request, token)
    username = user['email'].split('@')[0]
    with SessionLocal() as session:
        user_access = UserCrud(db=session)
        perm_access = PermissionCrud(db=session)
        dbuser = user_access.get_user_by_username(username)
        if dbuser is None:
            newuser = UserCreate(
                username=username, 
                email = user['email'], 
                displayname = user['name'])
            dbuser = user_access.create_user(newuser)
        perms = perm_access.get_user_permissions(dbuser.id)
        if perms is None:
            perms = PermissionsRead()

    # TODO: Create our own JWT here with claims?
    request.session['user'] = dict(user)
    return RedirectResponse(url='/')

@app.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)
    return RedirectResponse(url='/')

@app.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user is not None:
        u = json.dumps(user)
        html = (
            f'<pre>Email: {u}</pre><br>'
            '<a href="/docs">documentation</a><br>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')



async def get_user(request: Request) -> Optional[dict]:
    user = request.session.get('user')
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=403, detail='Could not validate credentials.')


@app.route('/openapi.json')
async def get_open_api_endpoint(request: Request, user: Optional[dict] = Depends(get_user)):  # This dependency protects our endpoint!
    response = JSONResponse(get_openapi(title='FastAPI', version=1, routes=app.routes))
    return response


@app.get('/docs', tags=['documentation'])  # Tag it as "documentation" for our docs
async def get_documentation(request: Request, user: Optional[dict] = Depends(get_user)):  # This dependency protects our endpoint!
    response = get_swagger_ui_html(openapi_url='/openapi.json', title='Documentation')
    return response