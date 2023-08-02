from sqlalchemy import TEXT, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models import Model


class RecommenderUser(Model):

    __tablename__ = "recommender_users"

    document_link = Column(TEXT, nullable=True)
    user_by_id = Column(
        String(),
        ForeignKey("users.id"),
        nullable=True)
    user_by = relationship("User", foreign_keys=user_by_id)
    user_id = Column(String(), ForeignKey("users.id"), nullable=True)
    user = relationship("User", foreign_keys=user_id)
