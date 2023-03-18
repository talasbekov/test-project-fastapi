from sqlalchemy.orm import relationship

from models import NamedModel
from models.association import user_liberations_liberations


class Liberation(NamedModel):

    __tablename__ = "liberations"

    user_liberations = relationship(
        "UserLiberation",
        secondary=user_liberations_liberations,
        back_populates='liberations',
        cascade="all,delete"
    )
