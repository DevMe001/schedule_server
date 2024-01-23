from pydantic import BaseModel, constr
from typing import List
from uuid import UUID


class AddressSchema(BaseModel):
    street: constr(min_length=1)