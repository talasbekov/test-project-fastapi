from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import TaxDeclaration
from schemas import TaxDeclarationCreate, TaxDeclarationUpdate
from services.base import ServiceBase


class TaxDeclarationService(ServiceBase[TaxDeclaration, TaxDeclarationCreate, TaxDeclarationUpdate]):

    def get_by_id(self, db: Session, id: str):
        tax_declaration = super().get(db, id)
        if tax_declaration is None:
            raise NotFoundException(detail=f"TaxDeclaration with id: {id} is not found!")
        return tax_declaration


tax_declaration_service = TaxDeclarationService(TaxDeclaration)
