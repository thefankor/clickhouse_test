from datetime import datetime
import uuid

from app.config import settings
from app.database import Base

from sqlalchemy import Column, Integer, String, Date, DateTime, UUID
from clickhouse_sqlalchemy import engines


class Events(Base):
    __tablename__ = 'events'
    __table_args__ = (
        engines.MergeTree(order_by=['timestamp', 'id']),
        {'schema': settings.DATABASE_NAME},
    )
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(Integer)
