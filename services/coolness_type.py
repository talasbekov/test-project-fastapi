from typing import Union, Dict, Any

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import CoolnessType
from schemas import CoolnessTypeCreate, CoolnessTypeUpdate
from .base import ServiceBase


class CoolnessTypeService(
    ServiceBase[CoolnessType, CoolnessTypeCreate, CoolnessTypeUpdate]):

    def get_by_id(self, db: Session, id: str):
        coolness_type = super().get(db, id)
        if coolness_type is None:
            raise NotFoundException(
                detail=f"Coolness with id: {id} is not found!")
        return coolness_type

    def get_all(self, db: Session, skip: int, limit: int, filter: str):
        coolness_types = db.query(CoolnessType)

        if filter != '':
            coolness_types = self._add_filter_to_query(coolness_types, filter)

        coolness_types = (coolness_types
                          .order_by(func.to_char(CoolnessType.name))
                          .offset(skip)
                          .limit(limit)
                          .all())

        total = db.query(CoolnessType).count()

        return {'total': total, 'objects': coolness_types}

    def _add_filter_to_query(self, coolness_type_query, filter):
        key_words = filter.lower().split()
        coolness_types = (
            coolness_type_query
            .filter(
                and_(func.concat(func.concat(func.lower(CoolnessType.name), ' '),
                                 func.concat(func.lower(CoolnessType.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return coolness_types


coolness_type_service = CoolnessTypeService(CoolnessType)
