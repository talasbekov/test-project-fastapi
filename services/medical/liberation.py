from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions import client
from models.medical import Liberation
from schemas.medical import LiberationCreate, LiberationUpdate
from services import ServiceBase
from services.filter import add_filter_to_query


class LiberationService(
        ServiceBase[Liberation, LiberationUpdate, LiberationCreate]):
    
    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        liberations = db.query(Liberation)

        if filter != '':
            liberations = add_filter_to_query(liberations, filter)

        liberations = (liberations
                       .order_by(func.to_char(Liberation.name))
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = db.query(Liberation).count()

        return {'total': total, 'objects': liberations}
    
    def get_by_id(self, db: Session, id: str):
        liberation = super().get(db, id)
        if liberation is None:
            raise client.NotFoundException(detail="Liberation is not found!")
        return liberation


liberation_service = LiberationService(Liberation)
