from sqlalchemy import Column, String, TIMESTAMP, Enum, UUID, ForeignKey

from models import Model
from enum import Enum as BaseEnum


class ServiceIDStatus(BaseEnum):
    RECEIVED = "Получен"
    LOST = "Утерян"
    NOT_RECEIVED = "Не получен"


class ServiceID(Model):

    __tablename__ = "service_ids"

    number = Column('service_number', String, nullable=True)
    date_to = Column(TIMESTAMP(timezone=True), nullable=True)

    token_status = Column(Enum(ServiceIDStatus), nullable=True)
    id_status = Column(Enum(ServiceIDStatus), nullable=True)

    user_id = Column(String(), ForeignKey("users.id"))
