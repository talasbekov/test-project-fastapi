import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Contract, ContractType, User, ContractHistory
from schemas import ContractCreate, ContractRead, ContractUpdate, ContractTypeRead
from .base import ServiceBase


class ContractService(ServiceBase[Contract, ContractCreate, ContractUpdate]):

    def create_relation(self, db: Session, user_id: uuid.UUID,
                        type_id: uuid.UUID):
        contract = super().create(db, ContractCreate(type_id=type_id, user_id=user_id))
        return contract

    def get_by_option(self, db: Session, type: str,
                      id: uuid.UUID, skip: int, limit: int):
        if type == 'write':
            return [ContractTypeRead.from_orm(i).dict() for i in db.query(
                ContractType).offset(skip).limit(limit).all()]
        else:
            user = db.query(User).filter(User.id == id).first()
            if user is None:
                raise NotFoundException(
                    detail=f"User with id: {id} is not found!")
            return [ContractRead.from_orm(contract).dict()
                    for contract in user.contracts]

    def get_object(self, db: Session, id: str, type: str):
        if type == 'write':
            return db.query(ContractType).filter(ContractType.id == id).first()
        else:
            return db.query(Contract).filter(Contract.id == id).first().type

    def stop_relation(self, db: Session, user_id: uuid.UUID, id: uuid.UUID):
        db.query(ContractHistory).filter(ContractHistory.contract_id ==
                                         id).update({'date_to': datetime.now()})

    def exists_relation(self, db: Session, user_id: str,
                        contract_type_id: uuid.UUID):
        return (
            db.query(Contract)
            .filter(Contract.user_id == user_id)
            .filter(Contract.type_id == contract_type_id)
            .first()
        ) is not None


contract_service = ContractService(Contract)
