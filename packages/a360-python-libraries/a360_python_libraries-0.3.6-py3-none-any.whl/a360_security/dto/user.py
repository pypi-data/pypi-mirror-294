import uuid

from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    username: str
    email: EmailStr
    sub: uuid.UUID
    roles: list[str]

    class Config:
        from_attributes = True
