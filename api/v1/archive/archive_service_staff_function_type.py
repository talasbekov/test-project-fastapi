import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (ServiceArchiveStaffFunctionTypeRead,
                     NewServiceArchiveStaffFunctionTypeCreate,
                     NewServiceArchiveStaffFunctionTypeUpdate)
from services import service_archive_staff_function_type_service

router = APIRouter(
    prefix="/service_archive_staff_function_type",
    tags=["ServiceArchiveStaffFunctionType"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ServiceArchiveStaffFunctionTypeRead],
            summary="Get all ArchiveStaffFunction")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all ArchiveStaffFunction

       - **skip**: int - The number of ArchiveStaffFunction
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ArchiveStaffFunction
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return service_archive_staff_function_type_service.get_multi(
        db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ServiceArchiveStaffFunctionTypeRead,
             summary="Create ArchiveStaffFunction")
async def create(*,
                 db: Session = Depends(get_db),
                 body: NewServiceArchiveStaffFunctionTypeCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create ArchiveStaffFunction

        - **parent_group_id**: the id of the parent group.
            This parameter is optional.
        - **name**: required
        - **description**: a long description. This parameter is optional.
    """
    Authorize.jwt_required()
    return (
        service_archive_staff_function_type_service
        .create_archive_staff_function_type(db,
                                            body)
        )


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ServiceArchiveStaffFunctionTypeRead,
            summary="Get ArchiveStaffFunction by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get ArchiveStaffFunction by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return service_archive_staff_function_type_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ServiceArchiveStaffFunctionTypeRead,
            summary="Update ArchiveStaffFunction")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: NewServiceArchiveStaffFunctionTypeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update ArchiveStaffFunction

        - **id**: UUID - id of the ArchiveStaffFunction.
        - **parent_group_id**: the id of the parent group.
            This parameter is optional.
        - **name**: required
        - **description**: a long description.
            This parameter is optional.
    """
    Authorize.jwt_required()
    obj = service_archive_staff_function_type_service.get_by_id(db, str(id))
    return (
        service_archive_staff_function_type_service
        .update_archive_staff_function_type(db,
                                            obj,
                                            body)
        )


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete ArchiveStaffFunction")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authrorize: AuthJWT = Depends()
                 ):
    """
        Delete ArchiveStaffFunction

        - **id**: UUID - required
    """
    Authrorize.jwt_required()
    service_archive_staff_function_type_service.remove(db, str(id))
