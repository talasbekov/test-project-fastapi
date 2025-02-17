from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import FamilyStatus
from schemas import FamilyStatusCreate, FamilyStatusUpdate, FamilyStatusRead
from services import ServiceBase
from services.profile import profile_service


class FamilyStatusService(
        ServiceBase[FamilyStatus, FamilyStatusCreate, FamilyStatusUpdate]):

    def get_by_id(self, db: Session, id: str):
        family_status = super().get(db, id)
        if family_status is None:
            raise NotFoundException(
                detail=f"FamilyStatus with id: {id} is not found!")
        return family_status

    def get_by_user_id(self, db: Session, id: str) -> FamilyStatusRead:
        profile = profile_service.get_by_user_id(db, id)
        
        if profile.personal_profile and profile.personal_profile.biographic_info and profile.personal_profile.biographic_info.family_status:
            family_status = profile.personal_profile.biographic_info.family_status
            return FamilyStatusRead.from_orm(family_status)
        else:
            raise NotFoundException(detail="Family status not found")

    def _validate_gender(self, dict1: dict, gender: bool):
        if dict1['name'] and dict1['nameKZ']:
            if gender == 1:
                dict1['name'] = dict1['name'].split(' / ')[0]
                dict1['nameKZ'] = dict1['nameKZ'].split(' / ')[0]
            else:
                dict1['name'] = dict1['name'].split(' / ')[1]
                dict1['nameKZ'] = dict1['nameKZ'].split(' / ')[1]

        return dict


family_status_service = FamilyStatusService(FamilyStatus)
