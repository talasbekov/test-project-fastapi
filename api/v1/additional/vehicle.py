from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from schemas import VehicleCreate, VehicleRead, VehicleUpdate
from core import get_db, configs
from services import vehicle_service, profile_service
from exceptions import SgoErpException
from typing import List
import uuid

router = APIRouter(prefix="/vehicle", tags=["Vehicle"], dependencies=[Depends(HTTPBearer())])

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
        Get all Abroad Travel

        - **skip**: int - The number of abroad travel to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of abroad travel to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject() 
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
        Create new abroad travel

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
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get abroad travel by id

        - **skip**: int - The number of abroad travel to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of abroad travel to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return vehicle_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=VehicleRead,
            summary="Update Vehicle by id")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: VehicleUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update abroad travel by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject() 
    profile = profile_service.get_by_user_id(db, credentials)
    vehicle = vehicle_service.get_by_id(db, id)
    if vehicle.profile_id != profile.id: # TODO: check role logic
        raise SgoErpException("You don't have permission to update this abroad travel")
    return vehicle_service.update(db, vehicle, body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=VehicleRead,
            summary="Delete Vehicle by id")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete abroad travel by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject()
    profile = profile_service.get_by_user_id(db, credentials)
    abroad_travel = vehicle_service.get_by_id(db, id)
    if abroad_travel.profile_id != profile.id: # TODO: check role logic
        raise SgoErpException("You don't have permission to delete this abroad travel")
    return vehicle_service.delete(db, abroad_travel)


