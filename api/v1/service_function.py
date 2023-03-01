import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import ServiceFunctionCreate, ServiceFunctionUpdate, ServiceFunctionRead
from services import service_function_service

router = APIRouter(prefix="/service_function", tags=["ServiceFunction"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ServiceFunctionRead],
            summary="Get all ServiceFunctions")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
       Get all ServiceFunctions

       - **skip**: int - The number of ServiceFunction to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ServiceFunction to return in the response. This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return service_function_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ServiceFunctionRead,
             summary="Create ServiceFunction")
async def create(*,
    db: Session = Depends(get_db),
    body: ServiceFunctionCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create ServiceFunction

        - **name**: required
        - **service_function_type_id**: UUID - required. The id of service function type.
        - **spend_hours_per_week**: int - optional.
    """
    Authorize.jwt_required()
    return service_function_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ServiceFunctionRead,
            summary="Get ServiceFunction by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get ServiceFunction by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return service_function_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ServiceFunctionRead,
            summary="Update ServiceFunction")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: ServiceFunctionUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update ServiceFunction

        - **name**: required
        - **service_function_type_id**: UUID - required. The id of service function type.
        - **spend_hours_per_week**: int - optional.
    """
    Authorize.jwt_required()
    return service_function_service.update(
        db,
        db_obj=service_function_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete ServiceFunction")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete ServiceFunction

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    service_function_service.remove(db, id)
