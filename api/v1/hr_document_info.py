import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (HrDocumentInfoCreate, HrDocumentInfoRead,
                     HrDocumentInfoUpdate, HrDocumentHistoryRead)
from services import hr_document_info_service

router = APIRouter(
    prefix="/hr-documents-info",
    tags=["HrDocumentInfos"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", response_model=List[HrDocumentInfoRead],
            summary="Get all HrDocumentInfo")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    """
        Get all HrDocumentInfo

    - **skip**: int - The number of HrDocumentInfo
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of HrDocumentInfo
        to return in the response.
        This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return hr_document_info_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             response_model=HrDocumentInfoRead,
             summary="Create HrDocumentInfo")
async def create(*,
                 db: Session = Depends(get_db),
                 body: HrDocumentInfoCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create HrDocumentInfo

        - **hr_document_step_id**: UUID - the id of HrDocumentStep associated
            with this document info. This is required.
        - **signed_by**: UUID - the id of the user who signed this document info.
            This field is optional.
        - **comment**: a comment regarding this document info.
        - **is_signed**: bool - whether or not this document info has been signed.
        - **hr_document_id**: UUID - the id of the HrDocument associated
            with this document info.
        - **signed_at**: the datetime at which this document info was signed.
            This field is optional. Format (YYYY-MM-DD)
    """
    Authorize.jwt_required()
    return hr_document_info_service.create(db, body)


@router.put("/{id}/", response_model=HrDocumentInfoRead,
            summary="Update HrDocumentInfo")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: HrDocumentInfoUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update HrDocumentInfo

    - **id**: UUID - the id of the HrDocumentInfo. This is required.
    - **hr_document_step_id**: UUID - the id of HrDocumentStep associated
        with this document info. This is required.
    - **signed_by**: UUID - the id of the user who signed this document info.
        This field is optional.
    - **comment**: a comment regarding this document info.
    - **is_signed**: bool - whether or not this document info has been signed.
    - **hr_document_id**: UUID - the id of the HrDocument
        associated with this document info.
    - **signed_at**: the datetime at which this document info was signed.
        This field is optional. Format (YYYY-MM-DD)
    """
    Authorize.jwt_required()
    return hr_document_info_service.update(
        db=db,
        db_obj=hr_document_info_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete HrDocumentInfo")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete HrDocumentInfo

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    hr_document_info_service.remove(db, id)


@router.get("/{id}/", status_code=status.HTTP_200_OK,
            summary="Get HrDocumentInfo by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get HrDocumentInfo by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return hr_document_info_service.get_by_id(db, id)


@router.get('/history/{id}/', response_model=List[HrDocumentHistoryRead],
            summary="Get History by document id")
async def get_history_by_document_id(*,
                                     db: Session = Depends(get_db),
                                     id: uuid.UUID,
                                     Authorize: AuthJWT = Depends()
                                     ):
    """
        Get History by document id

        The function returns a list of HrDocumentHistoryRead objects,
        which represent the history of the HR document.

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return hr_document_info_service.get_by_document_id(db, id)
