from pydantic import BaseModel, constr, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=50)
    first_name: constr(min_length=4, max_length=25)
    last_name: constr(min_length=4, max_length=25)
    usertype: constr(min_length=4, max_length=25)
