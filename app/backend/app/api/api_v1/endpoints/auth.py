from typing import Any

from fastapi import APIRouter, Request, Depends, HTTPException, status
from google import oauth2
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.backend.app.api  import deps
from app.backend.app.core.settings import settings
from app.backend.app.data.user import UserAccess, User
from app.backend.app.core.security import create_access_token
from authlib.integrations.starlette_client import OAuth, OAuthError
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import timedelta

router = APIRouter()
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id = settings['GOOGLE_CLIENT_ID'],
    client_secret = settings['GOOGLE_CLIENT_SECRET'],
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router.get('/login', tags=['authentication'])
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth2.google.authorize_redirect(
        request, 
        redirect_uri,
        login_hint="skyspook@dallasmakerspace.org", 
        hd='dallasmakerspace.org'
    )



@router.get('/auth')
async def auth(request: Request, dbsession = Depends(deps.get_db)):
    try:
        if request.method == 'GET' and 'code' in request.query_params:
            token = await oauth.google.authorize_access_token(request)
            user = await oauth.google.parse_id_token(request, token)
        elif request.method == 'POST':
            user = id_token.verify_oauth2_token(
                request.form['token'], 
                requests.Request(), 
                settings['GOOGLE_CLIENT_ID']
            )
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

@router.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)
    return RedirectResponse(url='/')