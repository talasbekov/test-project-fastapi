import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.medical import HospitalDataCreate,HospitalDataRead,HospitalDataUpdate
from services.medical import hospital_data_service

router = APIRouter(prefix="/hospital_data", tags=["HospitalData"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[HospitalDataRead],
            summary="Get all HospitalData")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all HospitalData

        - **skip**: int - The number of HospitalData to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of HospitalData to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return hospital_data_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=HospitalDataRead,
             summary="Create HospitalData")
async def create(*,
    db: Session = Depends(get_db),
    body: HospitalDataCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new HospitalData

        - **code**: str
        - **reason**: str
        - **place**: str
        - **start_date**: datetime.datetime
        - **end_date**: datetime.datetime
        - **document_link**: str
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return hospital_data_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=HospitalDataRead,
            summary="Get HospitalData by id")
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
            summary="Update HospitalData")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: HospitalDataUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update HospitalData

        - **id**: UUID - the ID of Hospital Data to update. This is required.
        - **code**: str
        - **reason**: str
        - **place**: str
        - **start_date**: datetime.datetime
        - **end_date**: datetime.datetime
        - **document_link**: str
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return hospital_data_service.update(
        db,
        db_obj=hospital_data_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete HospitalData")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete a HospitalData

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    hospital_data_service.remove(db, id)
