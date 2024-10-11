from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class AddEventType(str, Enum):
    apple_appears = "apple appears"
    cookie_appears = "cookie appears"
    cup_appears = "cup appears"
    mug_appears = "mug appears"
    face_appears = "face appears"


class EventType(int, Enum):
    apple_appears = 1
    cookie_appears = 2
    cup_appears = 3
    mug_appears = 4
    face_appears = 5

    @classmethod
    def to_string(cls, event_type: int) -> str:
        return cls(event_type).name.replace("_", " ")

    @classmethod
    def from_string(cls, event_string: str) -> 'EventType':
        # print(event_string)
        try:
            return cls[event_string.replace(" ", "_")]
        except KeyError:
            raise ValueError(f"Invalid event type: {event_string}")


class SEvents(BaseModel):
    id: UUID
    timestamp: datetime
    event_type: AddEventType


class CountEvents(BaseModel):
    event_type: AddEventType
    count: int


class SEventAdd(BaseModel):
    event_type: AddEventType


class SEventDelete(BaseModel):
    id: UUID
