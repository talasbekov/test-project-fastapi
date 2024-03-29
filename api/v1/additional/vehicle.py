
import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import VehicleCreate, VehicleRead, VehicleUpdate
from services import vehicle_service

router = APIRouter(
    prefix="/vehicle",
    tags=["Vehicle"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[VehicleRead],
            summary="Get all Vehicles")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all vehicle

    - **skip**: int - The number of vehicle to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of vehicle to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return vehicle_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=VehicleRead,
             summary="Create Vehicle")
async def create(*,
                 db: Session = Depends(get_db),
                 body: VehicleCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new vehicle

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return vehicle_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=VehicleRead,
            summary="Get Vehicle by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get vehicle by id

    - **skip**: int - The number of vehicle to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of vehicle to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return vehicle_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=VehicleRead,
            summary="Update Vehicle by id")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: VehicleUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update abroad travel by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return vehicle_service.update(
        db,
        db_obj=vehicle_service.get_by_id(db, str(id)),
        obj_in=body
    )


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               response_model=VehicleRead,
               summary="Delete Vehicle by id")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete vehicle by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    vehicle = vehicle_service.get_by_id(db, str(id))
    return vehicle_service.remove(db=db, id=vehicle.id)
