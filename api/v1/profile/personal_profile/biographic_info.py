import uuid

from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import BiographicInfoCreate, BiographicInfoUpdate, BiographicInfoRead
from services import biographic_info_service

router = APIRouter(prefix="/biographic_info", tags=["BiographicInfo"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[BiographicInfoRead],
            summary="Get all BiographicInfo")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all BiographicInfo

    """
    Authorize.jwt_required()
    return biographic_info_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=BiographicInfoRead,
             summary="Create BiographicInfo")
async def create(*,
    db: Session = Depends(get_db),
    body: BiographicInfoCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new BiographicInfo

    """
    Authorize.jwt_required()
    return biographic_info_service.create(db, body)

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BiographicInfoRead,
            summary="Get BiographicInfo by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get BiographicInfo by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return biographic_info_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BiographicInfoRead,
            summary="Update BiographicInfo")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: BiographicInfoUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update BiographicInfo

    """
    Authorize.jwt_required()
    return biographic_info_service.update(
        db,
        db_obj=biographic_info_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete BiographicInfo")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete BiographicInfo

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    biographic_info_service.remove(db, id)
