
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from models import Model


class Hexagon(Model):

    __tablename__ = "hr_erp_hexagon"

    KP = Column(Integer)
    LS = Column(Integer)
    EC = Column(Integer)
    PZ = Column(Integer)
    OP = Column(Integer)
    FP = Column(Integer)

    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    user = relationship("User")
