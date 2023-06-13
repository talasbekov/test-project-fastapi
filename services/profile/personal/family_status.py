from ast import Pass
from math import e
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import FamilyStatus
from schemas import FamilyStatusCreate, FamilyStatusUpdate, FamilyStatusRead
from services.base import ServiceBase
from services.profile import profile_service

class FamilyStatusService(ServiceBase[FamilyStatus, FamilyStatusCreate, FamilyStatusUpdate]):

    def get_by_id(self, db: Session, id: str):
        family_status = super().get(db, id)
        if family_status is None:
            raise NotFoundException(detail=f"FamilyStatus with id: {id} is not found!")
        return family_status
    
    def get_by_user_id(self, db: Session, id: str):
        profile = profile_service.get_by_user_id(db, id)
        
        try:        
            res = FamilyStatusRead.from_orm(profile.personal_profile.biographic_info.family_status).dict()
        except:
            return None
        
        if profile.personal_profile.biographic_info.gender == 1:
            res['name'] = res['name'].split(' / ')[0]
            res['nameKZ'] = res['nameKZ'].split(' / ')[0]
        else:
            res['name'] = res['name'].split(' / ')[1]
            res['nameKZ'] = res['nameKZ'].split(' / ')[1]
        
        return res


family_status_service = FamilyStatusService(FamilyStatus)
