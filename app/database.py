from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings
conn_str = f'clickhouse://{settings.CLICKHOUSE_USER}:{settings.CLICKHOUSE_PASS}@{settings.CLICKHOUSE_HOST}:{settings.CLICKHOUSE_PORT}'
engine = create_engine(conn_str)
session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


