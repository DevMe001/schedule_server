from pydantic import BaseModel, constr
from typing import List
from uuid import UUID


class PhoneNumberSchema(BaseModel):
    number: constr(min_length=1)