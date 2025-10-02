from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    email: str
    name: str


class AuthResponse(BaseModel):
    token: str
