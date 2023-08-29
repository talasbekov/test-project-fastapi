import uuid

from sqlalchemy import text
from sqlalchemy.orm import Session

from models import ActivityDate
from schemas import ActivityDateCreate, ActivityDateUpdate
from services.base import ServiceBase


class ActivityDateService(ServiceBase[ActivityDate,
                                     ActivityDateCreate,
                                     ActivityDateUpdate]):
    def create(self, db: Session, body: ActivityDateCreate):
        params = {'activity_date': str(body.activity_date),
                  'id': str(uuid.uuid4())}
        db.execute(text("""
                        INSERT INTO HR_ERP_ACTIVITY_DATES
                        (activity_date, id)
                        VALUES(TO_DATE(:activity_date, 'YYYY-MM-DD'),
                               :id)
                        """),
                   params)

        activity_date = self.get_by_id(db, params['id'])

        return activity_date

activity_day_service = ActivityDateService(ActivityDate)
