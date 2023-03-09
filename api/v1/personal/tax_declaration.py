import uuid

from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import TaxDeclarationCreate, TaxDeclarationUpdate, TaxDeclarationRead
from services import tax_declaration_service

router = APIRouter(prefix="/tax_declaration", tags=["TaxDeclaration"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[TaxDeclarationRead],
            summary="Get all TaxDeclaration")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all TaxDeclaration

        - **skip**: int - The number of TaxDeclaration to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of TaxDeclaration to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return tax_declaration_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=TaxDeclarationRead,
             summary="Create TaxDeclaration")
async def create(*,
    db: Session = Depends(get_db),
    body: TaxDeclarationCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new TaxDeclaration

        - **id**: UUID - the ID of TaxDeclaration to update. This is required.
        - **year**: str
        - **is_paid**: bool
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return tax_declaration_service.create(db, body)

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=TaxDeclarationRead,
            summary="Get TaxDeclaration by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get TaxDeclaration by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return tax_declaration_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=TaxDeclarationRead,
            summary="Update TaxDeclaration")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: TaxDeclarationUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update TaxDeclaration

        - **year**: str
        - **is_paid**: bool
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return tax_declaration_service.update(
        db,
        db_obj=tax_declaration_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete TaxDeclaration")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete TaxDeclaration

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    tax_declaration_service.remove(db, id)
