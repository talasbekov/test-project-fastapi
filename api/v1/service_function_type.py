import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import ServiceFunctionTypeCreate, ServiceFunctionTypeUpdate, ServiceFunctionTypeRead
from services import service_function_type_service

router = APIRouter(prefix="/service_function_type", tags=["ServiceFunctionType"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ServiceFunctionTypeRead],
            summary="Get all ServiceFunctionType")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
       Get all ServiceFunctionType

       - **skip**: int - The number of ServiceFunctionType to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ServiceFunctionType to return in the response. This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return service_function_type_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ServiceFunctionTypeRead,
             summary="Create ServiceFunctionType")
async def create(*,
    db: Session = Depends(get_db),
    body: ServiceFunctionTypeCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create ServiceFunctionType

        - **name**: required
    """
    Authorize.jwt_required()
    return service_function_type_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ServiceFunctionTypeRead,
            summary="Get ServiceFunctionType by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get ServiceFunctionType by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return service_function_type_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ServiceFunctionTypeRead,
            summary="Update ServiceFunction")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: ServiceFunctionTypeUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update ServiceFunction

        - **id**: UUID - the ID of ServiceFunctionType to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return service_function_type_service.update(
        db,
        db_obj=service_function_type_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete ServiceFunctionType")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete ServiceFunctionType

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    service_function_type_service.remove(db, id)
