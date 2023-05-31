import datetime

from sqlalchemy.orm import Session

from core import configs
from models import User, ContractType, ContractHistory, HrDocument
from .base import BaseHandler
from services import contract_service, history_service
from exceptions import ForbiddenException, NotFoundException
from utils import convert_str_to_datetime


def get_last_by_user_id(db: Session, user_id: str):
    res = (
        db.query(ContractHistory)
        .filter(ContractHistory.user_id == user_id)
        .order_by(ContractHistory.date_to.desc())
        .first()
    )
    return res


class RenewContractHandler(BaseHandler):
    __handler__ = "renew_contract"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        contract_type, date_from, date_to = self.get_args(db, action, props)

        res = contract_service.create_relation(db, user.id, contract_type.id)
        user.contracts.append(res)

        if contract_type.is_finite:

            history = history_service.create_timeline_history(
                db, user.id, res, date_from, date_to
            )
        else:
            history = history_service.create_history(db, user.id, res)
        history.document_link = configs.GENERATE_IP + str(document.id)

        db.add(user)
        db.add(document)
        db.add(history)
        db.flush()

        return user
    
    def handle_validation(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        pass

    def get_args(
            self,
            db: Session,
            action: dict,
            props: dict,
    ):
        try:
            contract_type_id = props[action["contract"]["tagname"]]["value"]
            contract_type = db.query(ContractType).filter(
                ContractType.id == contract_type_id
            ).first()

            if not contract_type:
                raise NotFoundException(
                    detail="Contract type not found"
                )
            date_from = datetime.datetime.now()
            date_to = date_from.replace(date_from.year + contract_type.years)
        except:
            raise ForbiddenException(detail=f'Invalid props for action: {self.__handler__}')
        return contract_type, date_from, date_to

    def handle_response(self, db: Session,
                        action: dict,
                        properties: dict,
                        ):
        data = list(self.get_args(db, action, properties))
        return data


handler = RenewContractHandler()
