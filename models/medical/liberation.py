from sqlalchemy.orm import relationship

from models import NamedModel
from models.association import u_liber_liberations


class Liberation(NamedModel):

    __tablename__ = "hr_erp_liberations"

    user_liberations = relationship(
        "UserLiberation",
        secondary=u_liber_liberations,
        back_populates='liberations',
        cascade="all,delete"
    )
