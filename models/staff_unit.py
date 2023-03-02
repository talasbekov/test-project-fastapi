import uuid

from sqlalchemy import TEXT, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base

from .association import staff_unit_functions


class StaffUnit(Base):

    __tablename__ = "staff_units"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=True)
    max_rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"),
                         nullable=True)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    document_staff_functions = relationship(
        "DocumentStaffFunction",
        secondary=staff_unit_functions,
        backref='staff_units',
        cascade="all,delete"
    )

    service_staff_functions = relationship(
        "ServiceStaffFunction",
        secondary=staff_unit_functions,
        backref="staff_units",
        cascade="all,delete"
    )
