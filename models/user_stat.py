from sqlalchemy import Column, ForeignKey, Integer, String

from models import Model


class UserStat(Model):

    __tablename__ = "hr_erp_user_stats"

    user_id = Column(String(), ForeignKey("hr_erp_users.id"), nullable=True)
    physical_training = Column(Integer)
    fire_training = Column(Integer)
    attendance = Column(Integer)
    activity = Column(Integer)
    opinion_of_colleagues = Column(Integer)
    opinion_of_management = Column(Integer)
