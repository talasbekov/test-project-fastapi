from pydantic import BaseModel, EmailStr

from .user import UserBase


class LoginForm(BaseModel):
    email: EmailStr
    password: str


class RegistrationForm(UserBase):
    role_name: str
    password: str
    re_password: str
