from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import SportAchievement
from schemas import SportAchievementCreate, SportAchievementUpdate
from services.base import ServiceBase
from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class SportAchievementService(
        ServiceBase[SportAchievement, SportAchievementCreate, SportAchievementUpdate]):

    def get_by_id(self, db: Session, id: str):
        sport_achievement = super().get(db, id)
        if sport_achievement is None:
            raise NotFoundException(
                detail=f"SportAchievement with id: {id} is not found!")
        return sport_achievement

    def create(self, db: Session,
               obj_in: Union[SportAchievementCreate, Dict[str, Any]]) -> SportAchievement:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['assignment_date'] = datetime.strptime(obj_in_data['assignment_date'], '%Y-%m-%d')
        db_obj = self.model(**obj_in_data) 
        db.add(db_obj)
        db.flush()
        return db_obj

sport_achievement_service = SportAchievementService(SportAchievement)
