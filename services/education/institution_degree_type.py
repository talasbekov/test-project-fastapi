from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import InstitutionDegreeType
from schemas.education import InstitutionDegreeTypeCreate, InstitutionDegreeTypeUpdate
from services import ServiceBase
from services.filter import add_filter_to_query


class InstitutionDegreeTypeService(
        ServiceBase[InstitutionDegreeType,
                    InstitutionDegreeTypeCreate,
                    InstitutionDegreeTypeUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        institutions = db.query(InstitutionDegreeType)

        if filter != '':
            institutions = add_filter_to_query(institutions, filter, InstitutionDegreeType)

        institutions = (institutions
                       .order_by(func.to_char(InstitutionDegreeType.name))
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = db.query(InstitutionDegreeType).count()

        return {'total': total, 'objects': institutions}

    def get_by_id(self, db: Session, id: str):
        institution_degree_type = super().get(db, id)
        if institution_degree_type is None:
            raise NotFoundException(
                detail=f"InstitutionDegreeType with id: {id} is not found!")
        return institution_degree_type


institution_degree_type_service = InstitutionDegreeTypeService(
    InstitutionDegreeType)
