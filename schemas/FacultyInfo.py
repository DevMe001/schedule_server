from pydantic import BaseModel, constr
from typing import Optional


class FacultyInfoSchema(BaseModel):
    name: constr(min_length=4, max_length=100)
    status: constr(min_length=4, max_length=50)
    allowed_units: int
    preferred_schedule: constr(min_length=4, max_length=50)