from typing import List
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import MilitaryInstitution
from schemas import MilitaryInstitutionCreate, MilitaryInstitutionUpdate, MilitaryInstitutionRead, MilitaryInstitutionReadPagination
from services.base import ServiceBase

class MilitaryInstitutionService(ServiceBase[MilitaryInstitution, MilitaryInstitutionCreate, MilitaryInstitutionUpdate]):
    def get_all(self, db: Session, skip: int = 0, limit: int = 100):



        return {
            'total':db.query(MilitaryInstitution).count(),
            'objects':db.query(MilitaryInstitution).offset(skip).limit(limit).all()
        }



military_institution_service = MilitaryInstitutionService(MilitaryInstitution)
