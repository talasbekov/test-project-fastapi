from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import relationship

from models import Model, NamedModel


class ContractType(NamedModel):
    __tablename__ = "contract_types"
    is_finite = Column(Boolean, nullable=False)
    years = Column(Integer, nullable=False)

    contracts = relationship("Contract", back_populates="type")


class Contract(Model):
    __tablename__ = "contracts"

    type_id = Column(UUID(as_uuid=True), ForeignKey("contract_types.id"))
    type = relationship("ContractType", back_populates="contracts")

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="contracts")
