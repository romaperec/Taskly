from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://name:pass@localhost:5432/dbname"
    DB_ECHO: bool = False


db_config = DatabaseConfig()
