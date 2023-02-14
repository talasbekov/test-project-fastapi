import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import HrDocumentCreate, HrDocumentUpdate, HrDocumentRead
from services import hr_document_service

router = APIRouter(prefix="/hr-documents", tags=["HrDocuments"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[HrDocumentRead])
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hr_document_service.get_not_signed_documents(db, user_id, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())])
async def initialize(*,
    db: Session = Depends(get_db),
    body: HrDocumentCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()['role']
    return hr_document_service.initialize(db, body, user_id, role)

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
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

@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               response_model=HrDocumentRead)
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return hr_document_service.remove(db, id)


@router.post("/{id}/", status_code=status.HTTP_200_OK,
             dependencies=[Depends(HTTPBearer())],
             response_model=HrDocumentRead)
async def sign(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    comment: str,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    hr_document_service.sign(db, id, comment, user_id)


@router.get('/generate/{id}/', status_code=status.HTTP_200_OK,
            dependencies=[Depends(HTTPBearer())])
async def generate(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return hr_document_service.generate(db, id)
