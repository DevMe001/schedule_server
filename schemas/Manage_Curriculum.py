from pydantic import BaseModel, constr


class Manage_CurriculumSchema(BaseModel):
        name: constr(min_length=4, max_length=20)
        order: constr(min_length=1)
