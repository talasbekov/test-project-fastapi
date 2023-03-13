import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (DrivingLicenseCreate, DrivingLicenseRead,
                     DrivingLicenseUpdate)
from services import driving_license_service

router = APIRouter(prefix="/driving_license", tags=["DrivingLicense"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[DrivingLicenseRead],
            summary="Get all DrivingLicense")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all DrivingLicense

        - **skip**: int - The number of DrivingLicense to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of DrivingLicense to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return driving_license_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=DrivingLicenseRead,
             summary="Create DrivingLicense")
async def create(*,
    db: Session = Depends(get_db),
    body: DrivingLicenseCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new DrivingLicense

        - **document_number**: str
        - **category**: List[str]
        - **date_of_issue**: datetime.date
        - **date_to**: datetime.date
        - **document_link**: str
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return driving_license_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DrivingLicenseRead,
            summary="Get DrivingLicense by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get DrivingLicense by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return driving_license_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DrivingLicenseRead,
            summary="Update DrivingLicense")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: DrivingLicenseUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update DrivingLicense

        - **id**: UUID - the ID of DrivingLicense to update. This is required.
        - **document_number**: str
        - **category**: List[str]
        - **date_of_issue**: datetime.date
        - **date_to**: datetime.date
        - **document_link**: str
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return driving_license_service.update(
        db,
        db_obj=driving_license_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete DrivingLicense")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete DrivingLicense

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    driving_license_service.remove(db, id)
