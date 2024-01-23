from pydantic import BaseModel, constr


class YearLevelSchema(BaseModel):
    name: constr(min_length=4, max_length=50)
    order: constr(min_length=1)
