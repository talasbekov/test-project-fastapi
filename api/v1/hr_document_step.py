from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import HrDocumentStepCreate, HrDocumentStepUpdate, HrDocumentStepRead
from services import hr_document_step_service

router = APIRouter(prefix="/hr-documents-step", tags=["HrDocumentSteps"], dependencies=[Depends(HTTPBearer())])


@router.get("", response_model=List[HrDocumentStepRead])
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return hr_document_step_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=HrDocumentStepRead)
async def create(*,
    db: Session = Depends(get_db),
    body: HrDocumentStepCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return hr_document_step_service.create(db, body)


@router.put("/{id}/", response_model=HrDocumentStepRead)
async def update(*,
    db: Session = Depends(get_db),
    id: str,
    body: HrDocumentStepUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return hr_document_step_service.update(
        db=db,
        db_obj=hr_document_step_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_202_ACCEPTED)
async def delete(*,
    db: Session = Depends(get_db),
    id: str,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    hr_document_step_service.remove(db, id)
