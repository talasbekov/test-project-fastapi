import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (ServiceStaffFunctionCreate, ServiceStaffFunctionRead,
                     ServiceStaffFunctionUpdate)
from services import service_staff_function_service, user_service

router = APIRouter(prefix="/service_staff_function", tags=["ServiceStaffFunction"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ServiceStaffFunctionRead],
            summary="Get all ServiceStaffFunction")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
       Get all ServiceStaffFunction

       - **skip**: int - The number of ServiceStaffFunction to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ServiceStaffFunction to return in the response. This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return service_staff_function_service.get_by_user(db, user_service.get_by_id(db, user_id))


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ServiceStaffFunctionRead,
             summary="Create ServiceStaffFunction")
async def create(*,
    db: Session = Depends(get_db),
    body: ServiceStaffFunctionCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create ServiceStaffFunction

        - **name**: required
        - **service_function_type_id**: UUID - required. The id of service function type.
        - **spend_hours_per_week**: int - optional.
    """
    Authorize.jwt_required()
    return service_staff_function_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ServiceStaffFunctionRead,
            summary="Get ServiceStaffFunction by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get ServiceStaffFunction by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return service_staff_function_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ServiceStaffFunctionRead,
            summary="Update ServiceStaffFunction")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: ServiceStaffFunctionUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update ServiceStaffFunction

        - **name**: required
        - **service_function_type_id**: UUID - required. The id of service function type.
        - **spend_hours_per_week**: int - optional.
    """
    Authorize.jwt_required()
    return service_staff_function_service.update(
        db,
        db_obj=service_staff_function_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete ServiceStaffFunction")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete ServiceStaffFunction

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    service_staff_function_service.remove(db, id)
