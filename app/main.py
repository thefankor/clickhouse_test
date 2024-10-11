from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, Query

from app.dao import EventsDAO

from app.schemas import SEventAdd, SEventDelete, SEvents, CountEvents, EventType

app = FastAPI(
    title="Test ClickHouse App"
)


@app.on_event("startup")
def on_start_app():
    EventsDAO.init_db()


@app.get("/")
def home(
        time_from: datetime = Query(
    ..., description=f"Например, {(datetime.utcnow().replace(microsecond=0) - timedelta(days=14))}"
        ),
        time_to: datetime = Query(...,
            description=f"Например, {datetime.utcnow().replace(microsecond=0)}"
        ),

) -> List[CountEvents]:
    return EventsDAO.get_events_in_time(time_from, time_to)


@app.get("/events")
def all_events() -> List[SEvents]:
    return [{"id": event.id, "timestamp": event.timestamp, "event_type": EventType.to_string(event.event_type)}
            for event in EventsDAO.get_all()]


@app.post("/")
def add_event(event_data: SEventAdd):
    return EventsDAO.add(event_data.event_type)


@app.delete("/events")
def delete_event(event_data: SEventDelete):
    return EventsDAO.delete(event_data.id)
