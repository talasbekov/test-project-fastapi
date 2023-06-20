from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import FamilyStatus
from schemas import FamilyStatusCreate, FamilyStatusUpdate, FamilyStatusRead
from services.base import ServiceBase
from services.profile import profile_service


class FamilyStatusService(
        ServiceBase[FamilyStatus, FamilyStatusCreate, FamilyStatusUpdate]):

    def get_by_id(self, db: Session, id: str):
        family_status = super().get(db, id)
        if family_status is None:
            raise NotFoundException(
                detail=f"FamilyStatus with id: {id} is not found!")
        return family_status

    def get_by_user_id(self, db: Session, id: str):
        profile = profile_service.get_by_user_id(db, id)

        try:
            res = FamilyStatusRead.from_orm(
                profile.personal_profile.biographic_info.family_status).dict()
        except Exception:
            return None

        return self._validate_gender(
            res, profile.personal_profile.biographic_info.gender)

    def _validate_gender(self, dict: dict, gender: bool):
        if gender == 1:
            dict['name'] = dict['name'].split(' / ')[0]
            dict['nameKZ'] = dict['nameKZ'].split(' / ')[0]
        else:
            dict['name'] = dict['name'].split(' / ')[1]
            dict['nameKZ'] = dict['nameKZ'].split(' / ')[1]

        return dict


family_status_service = FamilyStatusService(FamilyStatus)
