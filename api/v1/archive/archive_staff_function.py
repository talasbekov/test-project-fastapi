import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (ArchiveStaffFunctionRead, NewArchiveStaffFunctionCreate,
                     NewArchiveStaffFunctionUpdate, AllArchiveStaffFunctionsRead)
from services import archive_staff_function_service

router = APIRouter(prefix="/archive_staff_function", tags=["ArchiveStaffFunction"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AllArchiveStaffFunctionsRead],
            summary="Get all StaffFunction")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
       Get all StaffFunction

       - **skip**: int - The number of StaffFunction to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of StaffFunction to return in the response. This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return archive_staff_function_service.get_all_staff_functions(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ArchiveStaffFunctionRead,
             summary="Create StaffFunction")
async def create(*,
    db: Session = Depends(get_db),
    body: NewArchiveStaffFunctionCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create StaffFunction

        - **name**: required
        - **service_function_type_id**: UUID - required. The id of service function type.
        - **spend_hours_per_week**: int - optional.
    """
    Authorize.jwt_required()
    archive_staff_function_service.get_by_id(body.type_id)
    return archive_staff_function_service.create_archive_staff_function(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ArchiveStaffFunctionRead,
            summary="Get StaffFunction by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get StaffFunction by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return archive_staff_function_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ArchiveStaffFunctionRead,
            summary="Update StaffFunction")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: NewArchiveStaffFunctionUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update StaffFunction

        - **name**: required
        - **service_function_type_id**: UUID - required. The id of service function type.
        - **spend_hours_per_week**: int - optional.
    """
    Authorize.jwt_required()
    return archive_staff_function_service.update_archive_staff_function(
        db,
        staff_function=archive_staff_function_service.get_by_id(db, id),
        body=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete StaffFunction")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete StaffFunction

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    archive_staff_function_service.remove(db, id)


@router.post('/duplicate/{id}/', status_code=status.HTTP_201_CREATED,
            response_model=ArchiveStaffFunctionRead)
async def duplicate(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Duplicate StaffFunction

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return archive_staff_function_service.duplicate(db, id)
