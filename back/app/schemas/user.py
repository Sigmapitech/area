import re
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints


class UserSchema(BaseModel):
    id: int
    email: str
    name: str

    model_config = ConfigDict(from_attributes=True)


PasswordStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=8,
        max_length=50,
        pattern=re.compile(
            r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        ),
    ),
]


class RegisterRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
    name: str


class AccountUpdateRequest(BaseModel):
    email: EmailStr | None = None
    name: str | None = None


class AccountUpdatePasswordRequest(BaseModel):
    new_password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
