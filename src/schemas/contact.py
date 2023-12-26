from datetime import date, datetime

from pydantic import BaseModel, EmailStr, PastDate, Field

from src.schemas.user import UserResponse


class ContactSchema(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    email: EmailStr = Field(min_length=5, max_length=50)
    phone_number: str = Field(min_length=2, max_length=20)
    birthday: PastDate = PastDate()
    description: str = Field(min_length=2, max_length=50)


class ContactResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    phone_number: str
    birthday: PastDate
    description: str
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None

    class Config:
        from_attributes = True

