from sqlalchemy.orm import relationship

from models import NamedModel
from models.association import u_liber_liberations


class Liberation(NamedModel):

    __tablename__ = "hr_erp_liberations"
