from typing import Union, Any
from app.backend.app.data.user import User
from datetime import timedelta, datetime
from app.backend.app.core.settings import settings
from authlib.jose import jwt
def read_file(filename):
  fh = open(filename, "r")
  try:
      return fh.read()
  finally:
      fh.close()

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
    key = read_file('./app/jwtRS256.key')
    encoded_jwt = jwt.encode(header, to_encode, key)
    return encoded_jwt

def get_user_from_token(token: str) -> User:
    payload = jwt.decode(token, read_file('./app/jwtRS256.key.pub'))
    token_data = User.parse_obj(payload)
    return token_data