from pydantic import BaseModel


class UserInfo(BaseModel):
    email: str
    name: str
    picture: str | None = None


class AuthResponse(BaseModel):
    message: str
    user: UserInfo | None = None
