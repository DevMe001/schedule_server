from pydantic import BaseModel, constr


class AcademicYearSchema(BaseModel):
    name: constr(min_length=4, max_length=20)
    order: constr(min_length=1)
