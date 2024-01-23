from pydantic import BaseModel, constr


class UpdateUserSchema(BaseModel):
    first_name: constr(min_length=4, max_length=25)
    last_name: constr(min_length=4, max_length=25)