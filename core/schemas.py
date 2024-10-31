from datetime import datetime
from pydantic import BaseModel, Field


def ResponseModel(data, message):
    return {
        "data": data,
        "message": message,
    }


class UserBase(BaseModel):
    id: str
    email: str
    full_name: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: str
    full_name: str


class CatBase(BaseModel):
    name: str
    nickname: str
    owner: UserBase

    class Config:
        orm_mode = True


class CatCreate(BaseModel):
    name: str
    nickname: str
    dob: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class CatUpdate(BaseModel):
    name: str
    nickname: str
    dob: datetime
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
