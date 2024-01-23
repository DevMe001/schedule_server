from pydantic import BaseModel, Field, validator, field_validator, datetime_parse
from datetime import time, datetime
from typing import List, Optional

class FacultyLoadingSchema(BaseModel):
    acadyear_id: Optional[str]
    semester_id: Optional[str]
    facultyname: str
    facultystatus: str
    rank: str
    course_code: str
    course_description: str
    units: str
    lec: str
    lab: str
    classname: str
    schedule: str
    roomname: str


class FacultyLoadingBulkSchema(BaseModel):
    facultyloadings: List[FacultyLoadingSchema]

class FacultySearchSchema(BaseModel):
    acadyear_id: Optional[str]
    semester_id: Optional[str]
    facultyname: Optional[str]