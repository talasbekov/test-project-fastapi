import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (DocumentStaffFunctionTypeCreate,
                     DocumentStaffFunctionTypeRead,
                     DocumentStaffFunctionTypeUpdate)
from services import document_staff_function_type_service

router = APIRouter(prefix="/document_function_type", tags=["DocumentStaffFunctionType"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[DocumentStaffFunctionTypeRead],
            summary="Get all ServiceStaffFunctionType")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
       Get all ServiceStaffFunctionType

       - **skip**: int - The number of ServiceStaffFunctionType to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ServiceStaffFunctionType to return in the response. This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return document_staff_function_type_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=DocumentStaffFunctionTypeRead,
             summary="Create ServiceStaffFunctionType")
async def create(*,
    db: Session = Depends(get_db),
    body: DocumentStaffFunctionTypeCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create ServiceStaffFunctionType

        - **name**: required
    """
    Authorize.jwt_required()
    return document_staff_function_type_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DocumentStaffFunctionTypeRead,
            summary="Get ServiceStaffFunctionType by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get ServiceStaffFunctionType by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return document_staff_function_type_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DocumentStaffFunctionTypeRead,
            summary="Update ServiceFunction")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: DocumentStaffFunctionTypeUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update ServiceFunction

        - **id**: UUID - the ID of ServiceStaffFunctionType to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return document_staff_function_type_service.update(
        db,
        db_obj=document_staff_function_type_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete ServiceStaffFunctionType")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete ServiceStaffFunctionType

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    document_staff_function_type_service.remove(db, id)
