from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import SportAchievement
from schemas import SportAchievementCreate, SportAchievementUpdate, SportAchievementRead

from services.base import ServiceBase


class SportAchievementService(ServiceBase[SportAchievement, SportAchievementCreate, SportAchievementUpdate]):

    def get_by_id(self, db: Session, id: str):
        sport_achievement = super().get(db, id)
        if sport_achievement is None:
            raise NotFoundException(detail=f"SportAchievement with id: {id} is not found!")
        return sport_achievement


sport_achievement_service = SportAchievementService(SportAchievement)
