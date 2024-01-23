# schemas/Curriculum.py
from pydantic import BaseModel, UUID4
from typing import List, Optional


class CurriculumSchema(BaseModel):
    curriculum_year_name: Optional[str]
    course_id: Optional[str]
    year_level_id: Optional[str]
    semester_id: Optional[str]
    subject_code: str
    subject_name: str
    pre_req: str = None
    co_req: str = None
    lecture_hours: int
    lab_hours: int
    units: int
    tuition_hours: int


class BulkCurriculumSchema(BaseModel):
    curricula: List[CurriculumSchema]


class CurriculumFilterSchema(BaseModel):
    curriculum_year_name: Optional[str]
    course_id: Optional[str]
    year_level_id: Optional[str]
    semester_id: Optional[str]


class CurriculumFilterAllSchema(BaseModel):
    course_id: Optional[str]
    curriculum_year_name: Optional[str]


class CurriculumSearchSubjectCode(BaseModel):
    course_id: Optional[str]
    curriculum_year_name: Optional[str]
    subject_code: Optional[str]
