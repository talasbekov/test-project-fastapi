from pydantic import BaseModel, EmailStr

from schemas import Model, NamedModel, ReadModel, ReadNamedModel

from .user import UserBase


class LoginForm(Model):
    email: EmailStr
    password: str


class RegistrationForm(Model):
    role_name: str
    password: str
    re_password: str
