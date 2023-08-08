from sqlalchemy import Column, ForeignKey, TEXT, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class Activity(NamedModel):
    __tablename__ = 'hr_erp_activities'

    # Properties
    parent_group_id = Column(String(), ForeignKey(
        "hr_erp_activities.id"), nullable=True)
    instructions = Column(TEXT())

    # Relationships
    children = relationship("Activity")
