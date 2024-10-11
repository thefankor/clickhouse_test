import uuid

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select, DDL, insert, func, inspect

from app.config import settings
from app.models import Events
from app.schemas import EventType

from app.database import session, engine


class EventsDAO:

    @classmethod
    def get_events_in_time(cls, time_from: str, time_to: str):
        print(time_from, time_to)
        with session() as s:
            query = select(
                    Events.event_type,
                    func.count().label('count')
                ).filter(Events.timestamp.between(time_from, time_to)).group_by(Events.event_type)
            result = s.execute(query)
            return [{"event_type": EventType.to_string(row.event_type), "count": row.count} for row in result]

    @classmethod
    def get_all(cls):
        with (session() as s):
            query = select(Events).order_by('timestamp')
            result = s.execute(query)
            r = result.scalars().all()
            # print(r)
            return r

    @classmethod
    def add(cls, event_type):
        try:
            event_type = EventType.from_string(event_type)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        with session() as s:
            query = insert(Events).values(event_type=int(event_type))
            s.execute(query)
            s.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)

    @classmethod
    def delete(cls, event_id: uuid):
        with session() as s:
            event = s.query(Events).filter_by(id=event_id).first()
            if event:
                s.delete(event)
                s.commit()
                return None
            else:
                return HTTPException(status_code=404)

    @classmethod
    def init_db(cls):
        with session() as session4:
            session4.execute(DDL(f'CREATE DATABASE IF NOT EXISTS {settings.DATABASE_NAME}'))
            inspector = inspect(engine)
            if not inspector.has_table(Events.__tablename__, schema=settings.DATABASE_NAME):
                Events.__table__.create(engine)