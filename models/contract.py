from sqlalchemy import Column, ForeignKey, Boolean, String, Integer
from sqlalchemy.orm import relationship

from models import Model, NamedModel


class ContractType(NamedModel):
    __tablename__ = "hr_erp_contract_types"
    is_finite = Column(Boolean, nullable=False)
    years = Column(Integer, nullable=False)

    contracts = relationship("Contract", back_populates="type")


class Contract(Model):
    __tablename__ = "hr_erp_contracts"

    type_id = Column(String(), ForeignKey("hr_erp_contract_types.id"))
    type = relationship("ContractType", back_populates="contracts")

    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    user = relationship("User", back_populates="contracts")
