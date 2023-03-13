from sqlalchemy.orm import Session
from services import ServiceBase

from exceptions import client
from models.medical import AgeGroup
from schemas.medical import AgeGroupRead, AgeGroupUpdate, AgeGroupCreate


class AgeGroupService(ServiceBase[AgeGroup, AgeGroupCreate, AgeGroupUpdate]):
    def get_by_id(self, db: Session, id: str):
        age_group = super().get(db, id)
        if age_group is None:
            raise client.NotFoundException(detail="AgeGroup data is not found!")
        return age_group


age_group_service = AgeGroupService(AgeGroup)
