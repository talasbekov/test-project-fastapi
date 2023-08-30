from sqlalchemy import Column, ForeignKey, TEXT, String, Boolean
from sqlalchemy.orm import relationship


from models import NamedModel


class Activity(NamedModel):
    __tablename__ = 'hr_erp_activities'

    # Properties
    parent_group_id = Column(String(), ForeignKey(
        "hr_erp_activities.id"), nullable=True)
    instructions = Column(TEXT())
    is_time_required = Column(Boolean())
    normative_img = Column(TEXT(), nullable=True)

    # Relationships
    children = relationship("Activity")
