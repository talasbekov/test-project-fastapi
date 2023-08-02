from sqlalchemy import Column, ForeignKey, TEXT, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class Activity(NamedModel):
    __tablename__ = 'activities'

    # Properties
    parent_group_id = Column(String(), ForeignKey(
        "activities.id"), nullable=True)
    instructions = Column(TEXT())

    # Relationships
    children = relationship("Activity")
