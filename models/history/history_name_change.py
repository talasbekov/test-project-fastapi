from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship

from models import Model


class NameChange(Model):
    __tablename__ = "name_changes"

    name_before = Column(String, nullable=True)
    name_after = Column(String, nullable=True)
    name_type = Column(String, nullable=True)

    user_id = Column(String(), ForeignKey("users.id"))

    name_change_histories = relationship(
        "NameChangeHistory", back_populates="name_change")
