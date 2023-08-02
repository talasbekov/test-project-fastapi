from sqlalchemy import Column, ForeignKey, Boolean, String, Integer
from sqlalchemy.orm import relationship

from models import Model, NamedModel


class ContractType(NamedModel):
    __tablename__ = "contract_types"
    is_finite = Column(Boolean, nullable=False)
    years = Column(Integer, nullable=False)

    contracts = relationship("Contract", back_populates="type")


class Contract(Model):
    __tablename__ = "contracts"

    type_id = Column(String(), ForeignKey("contract_types.id"))
    type = relationship("ContractType", back_populates="contracts")

    user_id = Column(String(), ForeignKey("users.id"))
    user = relationship("User", back_populates="contracts")
