from pydantic import BaseModel, Field, validator, field_validator, datetime_parse
from datetime import time, datetime
from typing import List, Optional


class ScheduleSchema(BaseModel):
    acadyear_id: Optional[str]
    course_id: Optional[str]
    semester_id: Optional[str]
    class_id: Optional[str]
    subject_code: str
    subject_name: str
    lecture_hours: Optional[int]
    lab_hours: Optional[int]
    units: int
    tuition_hours: int
    day: str
    start_time: Optional[time] = Field(..., description="Format: HH:MM AM/PM")
    end_time: Optional[time] = Field(..., description="Format: HH:MM AM/PM")
    room_id: Optional[str]

    @field_validator("start_time", "end_time", mode="before")
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

    @field_validator("start_time", "end_time", mode="after")
    def validate_time_format(cls, value, values):
        if not isinstance(value, str):
            return value

        try:
            parsed_time = datetime.strptime(value, "%H:%M:%S").time()
            return parsed_time
        except ValueError:
            raise ValueError("Invalid time format. Use 'hh:mm:ss'.")

        return value


class BulkScheduleSchema(BaseModel):
    schedules: List[ScheduleSchema]


class ClassScheduleFilterSchema(BaseModel):
    acadyear_id: Optional[str]
    course_id: Optional[str]
    semester_id: Optional[str]
    class_id: Optional[str]

class RoomScheduleSchema(BaseModel):
    acadyear_id: Optional[str]
    semester_id: Optional[str]
    day: Optional[str]
    room_id: Optional[str]

class ScheduleSearchSubjectCode(BaseModel):
    acadyear_id: Optional[str]
    semester_id: Optional[str]
    subject_code: Optional[str]
