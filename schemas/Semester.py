from pydantic import BaseModel, constr


class SemesterSchema(BaseModel):
    name: constr(min_length=4, max_length=50)
    order: constr(min_length=1)
