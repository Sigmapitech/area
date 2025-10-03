from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: int
    email: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class AuthResponse(BaseModel):
    token: str
