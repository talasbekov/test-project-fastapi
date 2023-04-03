from sqlalchemy import TIMESTAMP, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TEXT, UUID

from models import NamedModel


class History(NamedModel):

    __tablename__ = "histories"

    date_from = Column(TIMESTAMP(timezone=True))
    date_to = Column(TIMESTAMP(timezone=True))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    type = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "history",
        "polymorphic_on": type,
    }


class StaffUnitHistory(History):

    staff_unit_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"))

    __mapper_args__ = {
        "polymorphic_identity": "staff_unit_history",
    }


class RankHistory(History):

    rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"))

    __mapper_args__ = {
        "polymorphic_identity": "rank_history",
    }


class PositionHistory(History):

    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"))

    __mapper_args__ = {
        "polymorphic_identity": "position_history",
    }


