import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (ScienceCreate,
                               ScienceRead,
                               ScienceUpdate,
                               ScienceReadPagination)
from services.education import science_service

router = APIRouter(prefix="/sciences",
                   tags=["Sciences"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=ScienceReadPagination,
            summary="Get all Sciences")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  filter: str = '',
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Sciences

    - **skip**: int - The number of Sciences
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of Sciences
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return science_service.get_all(db, skip, limit, filter)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ScienceRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: ScienceCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new Science

        - **name**: required
    """
    Authorize.jwt_required()
    return science_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ScienceRead,
            summary="Get Science by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Science by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return science_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ScienceRead,
            summary="Update Science")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: ScienceUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Science

        - **id**: UUID - the ID of Science to update.
            This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return science_service.update(
        db,
        db_obj=science_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Science")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Science

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    science_service.remove(db, str(id))
