from sqlalchemy import BigInteger, Column
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel
from .association import hr_document_equipments


class Equipment(NamedModel, Base):

    __tablename__ = "equipments"

    quantity = Column(BigInteger, nullable=True)
    hr_documents = relationship("HrDocument", secondary=hr_document_equipments,
                                back_populates="equipments")
