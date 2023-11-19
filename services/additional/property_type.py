from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import PropertyType, Profile
from schemas import PropertyTypeCreate, PropertyTypeUpdate
from services import profile_service
from services.base import ServiceBase


class PropertyTypeService(
        ServiceBase[PropertyType, PropertyTypeCreate, PropertyTypeUpdate]):

    def get_by_id(self, db: Session, id: str):
        property_type = super().get(db, id)
        if property_type is None:
            raise NotFoundException(
                detail=f"Property type with id: {id} is not found!")
        return property_type

    def get_multi_by_user_id(
            self, db: Session, user_id: str, skip: int = 0, limit: int = 100, filter: str = ''):
        profile: Profile = profile_service.get_by_user_id(db, user_id)
        if profile is None:
            raise NotFoundException(
                detail=f"Profile with user_id: {user_id} is not found!")

        properties = db.query(PropertyType)

        if filter != '':
            properties = self._add_filter_to_query(properties, filter)

        properties = (properties
                        .order_by(func.to_char(PropertyType.name))
                        .offset(skip)
                        .limit(limit)
                        .all())
        count = db.query(PropertyType).count()

        return {"total": count, "objects": properties}

    def _add_filter_to_query(self, property_type_query, filter):
        key_words = filter.lower().split()
        properties = (
            property_type_query
            .filter(
                and_(func.concat(func.concat(func.lower(PropertyType.name), ' '),
                                 func.concat(func.lower(PropertyType.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return properties

property_type_service = PropertyTypeService(PropertyType)
