from pydantic_settings import BaseSettings


class JWTConfig(BaseSettings):
    authjwt_secret_key: str = "qwerty123"
    authjwt_algorithm: str = "HS256"
