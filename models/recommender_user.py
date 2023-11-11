from sqlalchemy import TEXT, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models import Model


class RecommenderUser(Model):

    __tablename__ = "hr_erp_recommender_users"

    document_link = Column(TEXT, nullable=True)
    user_by_id = Column(
        String(),
        ForeignKey("hr_erp_users.id"),
        nullable=True)
    recommendant = Column(String(500), nullable=True)
    researcher = Column(String(500), nullable=True)
    user_by = relationship("User", foreign_keys=user_by_id)
    user_id = Column(String(), ForeignKey("hr_erp_users.id"), nullable=True)
    user = relationship("User", foreign_keys=user_id)
