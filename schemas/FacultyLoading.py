from pydantic import BaseModel, Field, validator, field_validator, datetime_parse
from datetime import time, datetime
from typing import List, Optional


class FacultyLoadingSchema(BaseModel):
    acadyear_id: Optional[str]
    semester_id: Optional[str]
    facultyid: int
    facultystatus: str
    totalunits: Optional[int]
    totalhours: Optional[int]
    ts: Optional[int]
    rank: str
    course_code: str
    course_description: str
    units: str
    tuition_hours: str
    lec: str
    lab: str
    day: str
    fstart_time: Optional[time] = Field(..., description="Format: HH:MM AM/PM")
    fend_time: Optional[time] = Field(..., description="Format: HH:MM AM/PM")
    classname: str
    roomname: Optional[str]

    @field_validator("fstart_time", "fend_time", mode="before")
    def parse_time(cls, value, values):
        if isinstance(value, str):
            # Strip leading and trailing whitespaces
            value = value.strip()
            try:
                parsed_time = datetime.strptime(value, "%I:%M %p").time()
                return parsed_time
            except ValueError:
                raise ValueError("Invalid time format. Use 'hh:mm am/pm'.")
        return value

    @field_validator("fstart_time", "fend_time", mode="after")
    def validate_time_format(cls, value, values):
        if not isinstance(value, str):
            return value

        try:
            parsed_time = datetime.strptime(value, "%H:%M:%S").time()
            return parsed_time
        except ValueError:
            raise ValueError("Invalid time format. Use 'hh:mm:ss'.")

        return value


class FacultyLoadingBulkSchema(BaseModel):
    facultyloadings: List[FacultyLoadingSchema]


class FacultySearchSchema(BaseModel):
    acadyear_id: Optional[str]
    semester_id: Optional[str]
    facultyid: Optional[int]


class SearchRoomWithFaculty(BaseModel):
    acadyear_id: Optional[str]
    semester_id: Optional[str]
    roomname: Optional[str]

class FacultyscheduleDay(BaseModel):
    acadyear_id: Optional[str]
    semester_id: Optional[str]
    facultyid: Optional[int]
    day: Optional[str]
