import uuid
from sqlalchemy.orm import Session
from exceptions.client import NotFoundException

from models import (ArchivePosition)
from schemas import ArchivePositionCreate, ArchivePositionUpdate, ArchivePositionAutoCreate
from services import ServiceBase


class ArchivePositionService(ServiceBase[ArchivePosition, ArchivePositionCreate, ArchivePositionUpdate]):

    def get_by_name(self, db: Session, name: str):
        role = db.query(ArchivePosition).filter(
            ArchivePosition.name == name
        ).first()

        if role:
            return role.id
        else:
            return None
        
    # def get_positions(self, db: Session, staff_list_id: uuid.UUID, skip: int = 0, limit: int = 100):
    #     return db.query(self.model).filter(
    #         ArchivePosition.staff_list_id == staff_list_id,
    #         ArchivePosition.parent_group_id == None,
    #     ).offset(skip).limit(limit).all()
        
    def get_by_origin_id(self, db: Session, id: uuid.UUID):
        position = db.query(self.model).filter(
            ArchivePosition.origin_id == id
        ).first()
        if position is None:
            raise NotFoundException(detail=f"Position with id {id} not found!")
        return position

    def create_based_on_existing_position(self, db: Session,
                                          name: str,
                                          nameKZ: str,
                                          category_code: str,
                                          max_rank_id: uuid.UUID,
                                          origin_id: uuid.UUID):
        return super().create(db, ArchivePositionAutoCreate(
            name=name,
            nameKZ=nameKZ,
            category_code=category_code,
            max_rank_id=max_rank_id,
            origin_id=origin_id
        ))

archive_position_service = ArchivePositionService(ArchivePosition)  # type: ignore
