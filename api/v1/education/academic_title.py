import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (AcademicTitleCreate,
                               AcademicTitleRead,
                               AcademicTitleUpdate)
from services.education import academic_title_service

router = APIRouter(prefix="/academic_titles",
                   tags=["AcademicTitles"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AcademicTitleRead],
            summary="Get all AcademicTitles")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all AcademicTitles

        - **skip**: int - The number of AcademicTitles to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of AcademicTitles to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return academic_title_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=AcademicTitleRead,
             summary="Create")
async def create(*,
    db: Session = Depends(get_db),
    body: AcademicTitleCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new AcademicTitle

        - **name**: required
    """
    Authorize.jwt_required()
    return academic_title_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AcademicTitleRead,
            summary="Get AcademicTitle by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get AcademicTitle by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return academic_title_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AcademicTitleRead,
            summary="Update AcademicTitle")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: AcademicTitleUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update AcademicTitle

        - **id**: UUID - the ID of AcademicTitle to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return academic_title_service.update(
        db,
        db_obj=academic_title_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete AcademicTitle")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete AcademicTitle

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    academic_title_service.remove(db, id)
