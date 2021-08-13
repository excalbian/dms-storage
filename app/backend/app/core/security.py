from enum import Enum
from typing import Union, Any
from app.data.user import User
from datetime import timedelta, datetime
from app.core.settings import settings
from authlib.jose import jwt

from ldap3 import Server, Connection

class NotAuthorizedException(Exception):
    pass

def read_file(filename):
  fh = open(filename, "r")
  try:
      return fh.read()
  finally:
      fh.close()

__key = read_file(settings.JWT_RSA_PRIV)
__pub = read_file(settings.JWT_RSA_PUB)

def create_access_token(
    subject: Union[str, Any], 
    expires_delta: timedelta = None, 
    user: User = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    header = {'alg': 'RS256'}
    to_encode = {
        "iss": "dms-storage",
        "exp": expire, 
        "sub": str(subject)}
    to_encode.update(dict(user))
    encoded_jwt = jwt.encode(header, to_encode, __key)
    return encoded_jwt

def get_user_from_token(token: str) -> User:
    payload = jwt.decode(token, __pub )
    token_data = User.parse_obj(payload)
    return token_data

def ad_auth_user( username: str, password: str):
    server = Server(settings.AD_URL)
    conn = Connection(server,user=username + settings.AD_UPN,password=password)
    try:
        conn.bind()
    except:
        raise NotAuthorizedException()
    
    conn.search('dc=dms,dc=local', f'(userPrincipalName={username}{settings.AD_UPN})', attributes=['cn','mail','displayName'])
    member = conn.entries

    if len(member) == 0:
        raise NotAuthorizedException()

    return {
        "username": username,
        "name": member[0].displayName.value,
        "email": member[0].mail.value
    }
