import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (SpecialtyCreate,
                               SpecialtyRead,
                               SpecialtyReadPagination,
                               SpecialtyUpdate)
from services.education import specialty_service

router = APIRouter(prefix="/specialties",
                   tags=["Specialties"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=SpecialtyReadPagination,
            summary="Get all Specialties")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  filter: str = '',
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Specialties

    - **skip**: int - The number of Specialties
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of Specialties
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return specialty_service.get_all(db, skip, limit, filter)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=SpecialtyRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: SpecialtyCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new Specialty

        - **name**: required
    """
    Authorize.jwt_required()
    return specialty_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SpecialtyRead,
            summary="Get Specialty by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Specialty by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return specialty_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SpecialtyRead,
            summary="Update Specialty")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: SpecialtyUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Specialty

        - **id**: UUID - the ID of Specialty to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return specialty_service.update(
        db,
        db_obj=specialty_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Specialty")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Specialty

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    specialty_service.remove(db, str(id))
