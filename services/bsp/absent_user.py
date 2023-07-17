from models import AbsentUser
from schemas import AbsentUserCreate, AbsentUserUpdate
from services.base import ServiceBase


class AbsentUserService(ServiceBase[AbsentUser, AbsentUserCreate, AbsentUserUpdate]):
    pass

absent_user_service = AbsentUserService(AbsentUser)
