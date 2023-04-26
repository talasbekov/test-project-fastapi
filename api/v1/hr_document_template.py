import uuid
from typing import List, Dict

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import HrDocumentTemplateCreate, HrDocumentTemplateUpdate, HrDocumentTemplateRead, SuggestCorrections
from services import hr_document_template_service

router = APIRouter(prefix="/hr-documents-template", tags=["HrDocumentTemplates"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[HrDocumentTemplateRead],
            summary="Get all HrDocumentTemplate")
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    name: str = None,
    limit: int = 10
):
    """
        Get all HrDocumentTemplate

        - **skip**: int - The number of HrDocumentTemplate to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of HrDocumentTemplate to return in the response. This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return hr_document_template_service.get_all_by_name(db, name, skip, limit)


@router.get('/archive')
async def get_all_archived(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    return hr_document_template_service.get_all_archived(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HrDocumentTemplateRead,
             summary="Create HrDocumentTemplate")
async def create(*,
    db: Session = Depends(get_db),
    body: HrDocumentTemplateCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create HrDocumentTemplate

        - **name**: required
        - **path**: string - the current location of this document. This is required.
        - **subject_type**: int - the subject type of the HrDocumentTemplate. This field should necessarily accept one of the following types.
        - **properties**: Dict[str, dict] - details which will be replaced while creating HrDocument. This is required.

        - CANDIDATE = 1
        - EMPLOYEE = 2
        - PERSONNEL = 3
        - STAFF = 4
    """
    Authorize.jwt_required()
    return hr_document_template_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HrDocumentTemplateRead,
            summary="Get HrDocumentTemplate by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get HrDocumentTemplate by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return hr_document_template_service.get_by_id(db, id)


@router.get("/steps/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=Dict[int, str],
            summary="Get HrDocumentTemplate by step id")
async def get_steps_by_document_template_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get HrDocumentTemplate by step id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return hr_document_template_service.get_steps_by_document_template_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HrDocumentTemplateRead,
            summary="Update HrDocumentTemplate")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: HrDocumentTemplateUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update HrDocumentTeplate

        - **id**: UUID - required.
        - **name**: required
        - **path**: string - the current location of this document. This is required.
        - **subject_type**: int - the subject type of the HrDocumentTemplate. This field should necessarily accept one of the following types.
        - **properties**: Dict[str, dict] - details which will be replaced while creating HrDocument. This is required.

        * CANDIDATE = 1
        * EMPLOYEE = 2
        * PERSONNEL = 3
        * STAFF = 4
    """
    Authorize.jwt_required()
    return hr_document_template_service.update(
        db=db,
        db_obj=hr_document_template_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete HrDocumentTemplate")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete HrDocumentTemplate

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    hr_document_template_service.remove(db, id)


@router.get('/duplicate/{id}', status_code=status.HTTP_201_CREATED)
async def duplicate(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    hr_document_template_service.duplicate(db, id)

@router.post('/corrections/')
async def suggest_corrections(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    body: SuggestCorrections
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    await hr_document_template_service.suggest_corrections(db, body, current_user_id)
