import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Contract, ContractType
from schemas import ContractCreate, ContractRead, ContractUpdate
from .base import ServiceBase


class ContractService(ServiceBase[Contract, ContractCreate, ContractUpdate]):

    def create_relation(self, db: Session, user_id: uuid.UUID, type_id: uuid.UUID):
        contract = super().create(db, ContractCreate(type_id=type_id, user_id=user_id))
        return contract

    def get_by_option(self, db: Session, skip: int, limit: int):
        return [i for i in db.query(ContractType).offset(skip).limit(limit).all()]


contract_service = ContractService(Contract)
