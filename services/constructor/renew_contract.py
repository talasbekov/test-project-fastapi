import datetime

from sqlalchemy.orm import Session

from models import User, ContractType, ContractHistory
from .base import BaseHandler
from services import contract_service, history_service
from exceptions import ForbiddenException
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
        self, db: Session, user: User, action: dict, template_props: dict, props: dict
    ):
        tagname = action["contract"]["tagname"]
        if not contract_service.exists_relation(db, user.id, props[tagname]["value"]):
            raise ForbiddenException(
                f"This user: {user.first_name}, {user.last_name}, doesn't have any contract"
            )
        contract_type = (
            db.query(ContractType)
            .filter(ContractType.id == props[tagname]["value"])
        )

        last_contract = get_last_by_user_id(db, user.id)
        last_contract.to_date = datetime.datetime.now()
        db.add(last_contract)

        res = contract_service.create_relation(db, user.id, props[tagname]["value"])
        user.contracts.append(res)

        if contract_type.is_finite:
            date_from = datetime.datetime.now()
            date_to = date_from.replace(date_from.year + contract_type.years)

            history_service.create_timeline_history(db, user.id, res, date_from, date_to)
        else:
            history_service.create_history(db, user.id, res)

        db.add(user)
        db.flush()

        return user


handler = RenewContractHandler()
