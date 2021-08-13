import os
from typing import  List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator
from pydantic.types import FilePath
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    AD_URL: str = "ad.dallasmakerspace.org"
    AD_UPN: str = "@dms.local"
    JWT_RSA_PRIV: FilePath = basedir + "/../jwtRS256.key"
    JWT_RSA_PUB: FilePath = basedir + "/../jwtRS256.key.pub"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DATABASE_URL: str = "sqlite:///" + os.path.join(basedir, '../../../../.data/app.db')

    DEV_BYPASSAUTH_ONLYADMIN: bool = False

    class Config:
        case_sensitive = True


settings = Settings( basedir + "../.env")
