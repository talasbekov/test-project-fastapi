
import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import VehicleTypeCreate, VehicleTypeRead, VehicleTypeUpdate, VehicleTypeReadPagination
from services import vehicle_type_service

router = APIRouter(
    prefix="/vehicle_type",
    tags=["VehicleTypeType"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=VehicleTypeReadPagination,
            summary="Get all VehicleTypes")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  filter: str = '',
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all vehicle_type

    - **skip**: int - The number of vehicle_type to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of vehicle_type to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return vehicle_type_service.get_all(db, skip, limit, filter)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=VehicleTypeRead,
             summary="Create VehicleType")
async def create(*,
                 db: Session = Depends(get_db),
                 body: VehicleTypeCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new vehicle_type

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return vehicle_type_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=VehicleTypeRead,
            summary="Get VehicleType by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get vehicle_type by id

    - **skip**: int - The number of vehicle_type to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of vehicle_type to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return vehicle_type_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=VehicleTypeRead,
            summary="Update VehicleType by id")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: VehicleTypeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update abroad travel by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return vehicle_type_service.update(
        db,
        db_obj=vehicle_type_service.get_by_id(db, str(id)),
        obj_in=body
    )


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               response_model=VehicleTypeRead,
               summary="Delete VehicleType by id")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete vehicle_type by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    vehicle_type = vehicle_type_service.get_by_id(db, str(id))
    return vehicle_type_service.remove(db=db, id=vehicle_type.id)
