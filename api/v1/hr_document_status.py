import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (HrDocumentStatusRead)
from services import hr_document_status_service

router = APIRouter(
    prefix="/hr-document-status",
    tags=["HrDocumentStatus"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", response_model=List[HrDocumentStatusRead],
            summary="Get all HrDocumentStatus")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    """
        Get all HrDocumentStatus

        - **skip**: int - The number of HrDocumentStatus to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of HrDocumentStatus to return in the response. This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return hr_document_status_service.get_multi(db, skip, limit)


@router.get("/{id}/", status_code=status.HTTP_200_OK,
            summary="Get HrDocumentStatus by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get HrDocumentStatus by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return hr_document_status_service.get_by_id(db, id)
