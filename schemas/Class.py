# schemas/Curriculum.py
from pydantic import BaseModel, constr
from uuid import UUID

class ClassSchema(BaseModel):
    classname: constr(min_length=4, max_length=50)
    year_level_id: UUID
    course_id: UUID
    section_id: UUID
