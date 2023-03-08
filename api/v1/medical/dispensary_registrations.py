import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.medical import DispensaryRegistrationRead,DispensaryRegistrationCreate,DispensaryRegistrationUpdate
from services.medical import dispensary_registration_service

router = APIRouter(prefix="/dispensary_registration", tags=["Dispensary Registration"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[DispensaryRegistrationRead],
            summary="Get all Anthropometric Data")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all Dispensary Registration
        - **skip**: int - The number of Dispensary Registration to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Dispensary Registration to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return dispensary_registration_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=DispensaryRegistrationRead,
             summary="Create")
async def create(*,
    db: Session = Depends(get_db),
    body: DispensaryRegistrationCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new Dispensary Registration
        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return dispensary_registration_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DispensaryRegistrationRead,
            summary="Get Dispensary Registration by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Dispensary Registration by id
        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return dispensary_registration_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DispensaryRegistrationRead,
            summary="Update Dispensary Registration")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: DispensaryRegistrationUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update AcademicDegree
        - **id**: UUID - the ID of Anthropometric Data to update. This is required.
        - **name**: required.
        - **url**: image url. This parameter is required.
    """
    Authorize.jwt_required()
    return dispensary_registration_service.update(
        db,
        db_obj=dispensary_registration_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Dispensary Registration")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete a Dispensary Registration
        - **id**: UUId - required
    """
    Authorize.jwt_required()
    dispensary_registration_service.remove(db, id)
