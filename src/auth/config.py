from datetime import timedelta
from pydantic_settings import BaseSettings


class JWTConfig(BaseSettings):
    authjwt_secret_key: str = "qwerty123"
    authjwt_algorithm: str = "HS256"
    authjwt_access_token_expires: timedelta = timedelta(minutes=30)
