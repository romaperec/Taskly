from pydantic_settings import BaseSettings


class JWTConfig(BaseSettings):
    SECRET_KEY: str = "qwerty12345"
    ALGORITHM: str = "HS256"


jwt_config = JWTConfig()
