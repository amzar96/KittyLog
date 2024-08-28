from pydantic import BaseModel


def ResponseModel(data, message):
    return {
        "data": data,
        "message": message,
    }


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    email: str
    username: str


class CatBase(BaseModel):
    name: str
    nickname: str

    class Config:
        orm_mode = True
