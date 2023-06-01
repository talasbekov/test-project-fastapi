import uuid

from sqlalchemy.orm import Session

from exceptions import NotSupportedException


class BaseCategory:
    __handler__ = 0

    def handle(self, db: Session) -> list[uuid.UUID]:
        raise NotSupportedException(f"Don't use this class: {self.__class__.__name__} directly")


handler = BaseCategory()
