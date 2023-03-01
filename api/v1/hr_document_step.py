import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import HrDocumentStepCreate, HrDocumentStepUpdate, HrDocumentStepRead
from services import hr_document_step_service

router = APIRouter(prefix="/hr-documents-step", tags=["HrDocumentSteps"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[HrDocumentStepRead],
            summary="Get all HrDocumentStep")
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    """
        Get all HrDocumentStep

        - **skip**: int - The number of HrDocumentStep to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of HrDocumentStep to return in the response. This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return hr_document_step_service.get_initial_steps(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HrDocumentStepRead,
             summary="Create HrDocumentStep")
async def create(*,
    db: Session = Depends(get_db),
    body: HrDocumentStepCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Crete HrDocumentStep

        - **hr_document_template_id**: UUID - the id of HrDocumentTemplate. This step will depend to this template. This field is required.
        - **previous_step_id**: UUID - the id of previous HrDocumentStep. This parameter is optional.
        - **staff_unit_id**: UUID - the id of StaffUnit. This is required.
        - **staff_function_id**: UUID - the id of StaffFunction. This is required.
    """
    Authorize.jwt_required()
    return hr_document_step_service.create_step(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HrDocumentStepRead,
            summary="Get HrDocumentStep by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get HrDocumentStep by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return hr_document_step_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HrDocumentStepRead,
            summary="Update HrDocumentStep")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: HrDocumentStepUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update HrDocumentStep

        - **id**: UUID - required
        - **hr_document_template_id**: UUID - the id of HrDocumentTemplate. This step will depend on this template. This field is required.
        - **previous_step_id**: UUID - the id of previous HrDocumentStep. This parameter is optional.
        - **staff_unit_id**: UUID - the id of StaffUnit. This is required.
        - **staff_function_id**: UUID - the id of StaffFunction. This is required.

        > Note that child steps **can not change** template type,
        > and **template will be changed for every child steps** if you want to change template for parent step
    """
    Authorize.jwt_required()
    return hr_document_step_service.update_step(db=db, step_id=id, obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete HrDocumentStep")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete HrDocumentStep

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    hr_document_step_service.delete_step(db, id)
