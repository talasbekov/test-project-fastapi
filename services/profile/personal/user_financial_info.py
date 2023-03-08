from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import UserFinancialInfo
from schemas import UserFinancialInfoCreate, UserFinancialInfoUpdate, UserFinancialInfoRead

from services.base import ServiceBase


class UserFinancialInfoService(ServiceBase[UserFinancialInfo, UserFinancialInfoCreate, UserFinancialInfoUpdate]):

    def get_by_id(self, db: Session, id: str):
        user_financial_info = super().get(db, id)
        if user_financial_info is None:
            raise NotFoundException(detail=f"UserFinancialInfo with id: {id} is not found!")
        return user_financial_info


user_financial_info_service = UserFinancialInfoService(UserFinancialInfo)
