from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import UserOath
from schemas import UserOathCreate, UserOathUpdate
from .base import ServiceBase


class UserOathService(ServiceBase[UserOath, UserOathCreate, UserOathUpdate]):
    pass


user_oath_service = UserOathService(UserOath)
