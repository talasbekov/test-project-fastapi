
from sqlalchemy import Column, ForeignKey, String, Float
from sqlalchemy.orm import relationship

from models import Model


class Hexagon(Model):

    __tablename__ = "hr_erp_hexagon"

    KP = Column(Float)
    LS = Column(Float)
    EC = Column(Float)
    PZ = Column(Float)
    OP = Column(Float)
    FP = Column(Float)

    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    user = relationship("User")
