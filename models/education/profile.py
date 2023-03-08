from sqlalchemy.orm import relationship

from core import Base
from models import Model


class Profile(Model, Base):

    __tablename__ = "profiles"
