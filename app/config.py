from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASS: str
    DATABASE_NAME: str
    TABLE_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()