from pydantic import BaseModel, constr
from typing import Optional


class RoomSchema(BaseModel):
    room_building: constr(min_length=1)
    room_number: str
    is_lab: bool