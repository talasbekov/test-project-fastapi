from sqlalchemy.orm import Session

from models import (Position, ArchivePosition)
from schemas import PositionCreate, PositionUpdate
from services import ServiceBase


class PositionService(ServiceBase[Position, PositionCreate, PositionUpdate]):

    def get_by_name(self, db: Session, name: str):
        role = db.query(Position).filter(
            Position.name == name
        ).first()

        if role:
            return role.id
        else:
            return None

    def create_from_archive(self, db: Session, archive_position: ArchivePosition):
        res = super().create(
            db, PositionCreate(
                name=archive_position.name,
                nameKZ=archive_position.nameKZ,
                category_code=archive_position.category_code,
                max_rank_id=archive_position.max_rank_id
                )
            )
        return res

    def update_from_archive(self, db: Session, archive_position: ArchivePosition):
        staff_unit = self.get_by_id(db, archive_position.origin_id)
        res = super().update(
            db,
            db_obj=staff_unit,
            obj_in=PositionUpdate(
                name=archive_position.name,
                nameKZ=archive_position.nameKZ,
                category_code=archive_position.category_code,
                max_rank_id=archive_position.max_rank_id
            )
        )
        return res

    def create_or_update_from_archive(self, db: Session, archive_position: ArchivePosition):
        if archive_position.origin_id is None:
            return self.create_from_archive(db, archive_position)
        return self.update_from_archive(db, archive_position)

position_service = PositionService(Position)  # type: ignore
