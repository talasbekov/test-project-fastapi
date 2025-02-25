from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Contract, ContractType, User, ContractHistory
from schemas import ContractCreate, ContractRead, ContractUpdate, ContractTypeRead
from services.filter import add_filter_to_query
from .base import ServiceBase


class ContractService(ServiceBase[Contract, ContractCreate, ContractUpdate]):

    def create_relation(self, db: Session, user_id: str,
                        type_id: str):
        contract = super().create(db, ContractCreate(type_id=type_id, user_id=user_id))
        return contract

    def get_by_option(self, db: Session, type: str,
                      id: str, skip: int, limit: int):
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

    def get_all_contract_types(self, db: Session, skip: int, limit: int, filter: str = ''):
        contract_types = db.query(ContractType).\
            filter(text("DBMS_LOB.SUBSTR(hr_erp_contract_types.name, 4000) != :contract_name")).\
            params(contract_name='Контракт')

        if filter != '':
            # Ensure your filtering logic also safely handles NCLOB conversion if necessary
            contract_types = add_filter_to_query(contract_types, filter, ContractType)

        # Fetching data and creating objects
        contract_types = [
            ContractTypeRead.from_orm(i).dict() for i in
            contract_types.order_by(ContractType.years.desc()).
            offset(skip).
            limit(limit).
            all()
        ]

        # Count query also needs to handle NCLOB properly
        total = db.query(ContractType).\
            filter(text("DBMS_LOB.SUBSTR(hr_erp_contract_types.name, 4000) != :contract_name")).\
            params(contract_name='Контракт').count()

        return {'total': total, 'objects': contract_types}
    
    def create_contract_type(self, db: Session, isFinite: bool, years: int, name: str, nameKZ: str):
        contract_type = ContractType(id=str(uuid.uuid4()), is_finite=isFinite, years=years, name=name, nameKZ=nameKZ)
        db.add(contract_type)
        db.commit()
        db.refresh(contract_type)
        return contract_type

    def get_object(self, db: Session, id: str, type: str):
        if type == 'write':
            return db.query(ContractType).filter(ContractType.id == id).first()
        else:
            return db.query(Contract).filter(Contract.id == id).first().type

    def stop_relation(self, db: Session, user_id: str, id: str):
        db.query(ContractHistory).filter(ContractHistory.contract_id ==
                                         id).update({'date_to': datetime.now()})

    def exists_relation(self, db: Session, user_id: str,
                        contract_type_id: str):
        return (
            db.query(Contract)
            .filter(Contract.user_id == user_id)
            .filter(Contract.type_id == contract_type_id)
            .first()
        ) is not None


contract_service = ContractService(Contract)
