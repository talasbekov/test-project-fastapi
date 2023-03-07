from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import PsychologicalCheck
from services.base import ServiceBase
from schemas import PsychologicalCheckCreate, PsychologicalCheckUpdate

class PsychologicalService(ServiceBase[PsychologicalCheck, PsychologicalCheckCreate, PsychologicalCheckUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"Violation with id: {id} is not found!")
        return rank
    
    def create(self, db: Session, obj_in: PsychologicalCheckCreate):
        return super().create(db, obj_in)
    
    def update(self, db: Session, db_obj: PsychologicalCheck, obj_in: PsychologicalCheckUpdate):
        return super().update(db, db_obj, obj_in)
    
    def delete(self, db: Session, id: str):
        return super().delete(db, id)


psychological_check_service = PsychologicalService(PsychologicalCheck)
