from sqlalchemy.orm import Session

from models import User, HrDocument
from .base import BaseHandler


class SuperDocHandler(BaseHandler):
    __handler__ = "superdoc"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        pass

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

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        pass


handler = SuperDocHandler()
