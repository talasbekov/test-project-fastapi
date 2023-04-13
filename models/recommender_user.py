from sqlalchemy import TEXT, Column, Integer, ForeignKey, UUID
from sqlalchemy.orm import relationship
from models import Model


class RecommenderUser(Model):

    __tablename__ = "recommender_users"

    document_link = Column(TEXT, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    user = relationship("User", foreign_keys=user_id)
    