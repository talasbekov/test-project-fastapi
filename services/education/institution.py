from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Institution
from schemas.education import InstitutionCreate, InstitutionUpdate
from services import ServiceBase
from services.filter import add_filter_to_query


class InstitutionService(
        ServiceBase[Institution, InstitutionCreate, InstitutionUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        institutions = db.query(Institution)

        if filter != '':
            institutions = add_filter_to_query(institutions, filter, Institution)

        institutions = (institutions
                       .order_by(func.to_char(Institution.name))
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = db.query(Institution).count()

        return {'total': total, 'objects': institutions}

    def get_by_id(self, db: Session, id: str):
        institution = super().get(db, id)
        if institution is None:
            raise NotFoundException(
                detail=f"Institution with id: {id} is not found!")
        return institution


institution_service = InstitutionService(Institution)
