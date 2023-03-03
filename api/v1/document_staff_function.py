import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (DocumentStaffFunctionCreate, DocumentStaffFunctionRead,
                     DocumentStaffFunctionUpdate)
from services import document_staff_function_service, user_service

router = APIRouter(prefix="/document_staff_function", tags=["DocumentStaffFunction"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[DocumentStaffFunctionRead],
            summary="Get all DocumentStaffFunction")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
       Get all DocumentStaffFunction

       - **skip**: int - The number of DocumentStaffFunction to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of DocumentStaffFunction to return in the response. This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return document_staff_function_service.get_by_user(db, user_service.get_by_id(db, user_id))


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DocumentStaffFunctionRead,
            summary="Get DocumentStaffFunction by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get DocumentStaffFunction by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return document_staff_function_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DocumentStaffFunctionRead,
            summary="Update DocumentStaffFunction")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: DocumentStaffFunctionUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update DocumentStaffFunction

    """
    Authorize.jwt_required()
    return document_staff_function_service.update(
        db,
        db_obj=document_staff_function_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete DocumentStaffFunction")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete DocumentStaffFunction

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    document_staff_function_service.remove(db, id)
