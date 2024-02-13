from sqlalchemy.orm import Session

from models import Activity
from schemas import ActivityCreate, ActivityUpdate
from services.base import ServiceBase


class ActivityService(ServiceBase[Activity, ActivityCreate, ActivityUpdate]):
    def get_all(self, db: Session, skip: int, limit: int):
        activities = (db.query(Activity)
                      .filter(Activity.parent_group_id == None)
                      .offset(skip)
                      .limit(limit)
                      .all())

        return activities

activity_service = ActivityService(Activity)
