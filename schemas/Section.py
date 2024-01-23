from pydantic import BaseModel, constr


class SectionSchema(BaseModel):
    name: constr(min_length=1, max_length=50)
    order: constr(min_length=1)
    description: constr(min_length=5)