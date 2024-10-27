from pydantic import BaseModel


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