import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (DrivingLicenseCreate, DrivingLicenseRead,
                     DrivingLicenseUpdate)
from services import driving_licence_service

router = APIRouter(prefix="/driving_licence", tags=["DrivingLicence"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[DrivingLicenseRead],
            summary="Get all DrivingLicence")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all DrivingLicence

    """
    Authorize.jwt_required()
    return driving_licence_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=DrivingLicenseRead,
             summary="Create DrivingLicence")
async def create(*,
    db: Session = Depends(get_db),
    body: DrivingLicenseCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new DrivingLicence

    """
    Authorize.jwt_required()
    return driving_licence_service.create(db, body)

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DrivingLicenseRead,
            summary="Get DrivingLicence by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get DrivingLicence by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return driving_licence_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DrivingLicenseRead,
            summary="Update DrivingLicence")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: DrivingLicenseUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update DrivingLicence

    """
    Authorize.jwt_required()
    return driving_licence_service.update(
        db,
        db_obj=driving_licence_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete DrivingLicence")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete DrivingLicence

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    driving_licence_service.remove(db, id)
