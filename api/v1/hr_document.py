import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import HrDocumentCreate, HrDocumentUpdate, HrDocumentRead, HrDocumentInit, HrDocumentSign
from services import hr_document_service

router = APIRouter(prefix="/hr-documents", tags=["HrDocuments"], dependencies=[Depends(HTTPBearer())])


@router.get("", response_model=List[HrDocumentRead])
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hr_document_service.get_not_signed_documents(db, user_id, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=HrDocumentRead)
async def initialize(*,
    db: Session = Depends(get_db),
    body: HrDocumentInit,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()['role']
    return hr_document_service.initialize(db, body, user_id, role)

@router.put("/{id}/",
            response_model=HrDocumentRead)
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: HrDocumentUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return hr_document_service.update(
        db=db,
        db_obj=hr_document_service.get_by_id(db, id),
        obj_in=body)

@router.delete("/{id}/", status_code=status.HTTP_202_ACCEPTED,
               response_model=HrDocumentRead)
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    hr_document_service.remove(db, id)


@router.post("/{id}/", status_code=status.HTTP_200_OK)
async def sign(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: HrDocumentSign,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()['role']
    hr_document_service.sign(db, id, body, user_id, role)


@router.get('/generate/{id}/', status_code=status.HTTP_200_OK)
async def generate(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return hr_document_service.generate(db, id)

@router.get("/check")
async def check(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    hr_document_service.get_multi(db)[0].properties
    return 
