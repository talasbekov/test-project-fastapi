from .base import BaseAutoTagHandler
from schemas import AutoTagRead
from services import user_service


class NameAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "name"

    def handle(self, db, user_id):
        user = user_service.get_by_id(db, user_id)
        return AutoTagRead(name=user.first_name, nameKZ=user.first_name)


handler = NameAutoTagHandler()
