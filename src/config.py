from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DB_URL: str = "postgresql+asyncpg://name:pass@localhost:5432/dbname"
    DB_ECHO: bool = False


db_config = DatabaseConfig()
