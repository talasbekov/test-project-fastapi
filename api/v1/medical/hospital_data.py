import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.medical import HospitalDataCreate,HospitalDataRead,HospitalDataUpdate
from services.medical import hospital_data_service

router = APIRouter(prefix="/hospital_data", tags=["Hospital Data"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[HospitalDataRead],
            summary="Get all Hospital Data") 
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all Hospital Data
        - **skip**: int - The number of Hospital Data to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Hospital Data to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return hospital_data_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HospitalDataRead,
             summary="Create Hospital Data")
async def create(*,
    db: Session = Depends(get_db),
    body: HospitalDataCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new Hospital Data
        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return hospital_data_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HospitalDataRead,
            summary="Get Hospital Data by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Hospital Data by id
        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return hospital_data_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model= HospitalDataRead,
            summary="Update Hospital Data")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: HospitalDataUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update Hospital Data
        - **id**: UUID - the ID of Hospital Data to update. This is required.
        - **name**: required.
        - **url**: image url. This parameter is required.
    """
    Authorize.jwt_required()
    return hospital_data_service.update(
        db,
        db_obj=hospital_data_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Hospital Data")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete a Hospital Data 
        - **id**: UUId - required
    """
    Authorize.jwt_required()
    hospital_data_service.remove(db, id)
