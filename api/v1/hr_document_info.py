import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (HrDocumentInfoCreate, HrDocumentInfoRead,
                     HrDocumentInfoUpdate)
from services import hr_document_info_service

router = APIRouter(prefix="/hr-documents-info", tags=["HrDocumentInfos"], dependencies=[Depends(HTTPBearer())])


@router.get("", response_model=List[HrDocumentInfoRead])
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return hr_document_info_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             response_model=HrDocumentInfoRead)
async def create(*,
    db: Session = Depends(get_db),
    body: HrDocumentInfoCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return hr_document_info_service.create(db, body)


@router.put("/{id}/", response_model=HrDocumentInfoRead)
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: HrDocumentInfoUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return hr_document_info_service.update(
        db=db,
        db_obj=hr_document_info_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    hr_document_info_service.remove(db, id)


@router.get("/{id}/", status_code=status.HTTP_200_OK)
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return hr_document_info_service.get_by_id(db, id)


@router.get('/history/{id}/', response_model= List[HrDocumentInfoRead])
async def get_history_by_document_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return hr_document_info_service.get_by_document_id(db, id)
