from pydantic import BaseModel, constr
from typing import Optional


class SubjectSchema(BaseModel):
    code: constr(min_length=4, max_length=50)
    name: constr(min_length=4, max_length=50)
