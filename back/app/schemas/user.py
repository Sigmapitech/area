from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    email: str
    name: str

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    token: str
