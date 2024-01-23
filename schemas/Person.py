from pydantic import BaseModel, constr
from typing import List
from uuid import UUID


class PersonSchema(BaseModel):
    name: constr(min_length=1)
    address_id: UUID
    phone_number_id: UUID

class PersonBulkCreateSchema(BaseModel):
    items: List[PersonSchema]
    