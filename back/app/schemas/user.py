import re
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

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


class UserSchema(BaseModel):
    id: int
    email: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class AuthResponse(BaseModel):
    token: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
    name: str


class AccountUpdateRequest(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    password: PasswordStr | None = None
    current_password: PasswordStr | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
