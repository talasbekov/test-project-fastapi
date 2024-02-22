from sqlalchemy import Column, String, TIMESTAMP, Enum, UUID, ForeignKey

from models import Model
from enum import Enum as BaseEnum


class ServiceIDStatus(BaseEnum):
    RECEIVED = "Получен"
    LOST = "Утерян"
    NOT_RECEIVED = "Не получен"


class ServiceID(Model):

    __tablename__ = "hr_erp_service_ids"

    number = Column('service_number', String, nullable=True)
    date_to = Column(TIMESTAMP(timezone=True), nullable=True)
    token_number = Column(String, nullable=True)
    token_status = Column(String, nullable=True)
    id_status = Column(String, nullable=True)

    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
