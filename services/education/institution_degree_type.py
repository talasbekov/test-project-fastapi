from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import InstitutionDegreeType
from schemas.education import InstitutionDegreeTypeCreate, InstitutionDegreeTypeUpdate
from services import ServiceBase


class InstitutionDegreeTypeService(
        ServiceBase[InstitutionDegreeType, 
                    InstitutionDegreeTypeCreate, 
                    InstitutionDegreeTypeUpdate]):

    def get_by_id(self, db: Session, id: str):
        institution_degree_type = super().get(db, id)
        if institution_degree_type is None:
            raise NotFoundException(
                detail=f"InstitutionDegreeType with id: {id} is not found!")
        return institution_degree_type


institution_degree_type_service = InstitutionDegreeTypeService(
    InstitutionDegreeType)
