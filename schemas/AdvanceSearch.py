from pydantic import BaseModel, UUID4

class AdvancedSearchQuery(BaseModel):
    curriculum_year_id: UUID4
    course_id: UUID4
    year_level_id: UUID4
    semester_id: UUID4
