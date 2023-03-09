import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (AcademicDegreeDegreeCreate,
                               AcademicDegreeDegreeRead,
                               AcademicDegreeDegreeUpdate)
from services.education import academic_degree_degree_service

router = APIRouter(prefix="/academic_degree_degrees",
                   tags=["AcademicDegreeDegrees"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AcademicDegreeDegreeRead],
            summary="Get all AcademicDegreeDegrees")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all AcademicDegreeDegrees

        - **skip**: int - The number of AcademicDegreeDegrees to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of AcademicDegreeDegrees to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return academic_degree_degree_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=AcademicDegreeDegreeRead,
             summary="Create")
async def create(*,
    db: Session = Depends(get_db),
    body: AcademicDegreeDegreeCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new AcademicDegreeDegree

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return academic_degree_degree_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AcademicDegreeDegreeRead,
            summary="Get AcademicDegreeDegree by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get AcademicDegreeDegree by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return academic_degree_degree_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AcademicDegreeDegreeRead,
            summary="Update AcademicDegreeDegree")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: AcademicDegreeDegreeUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update AcademicDegreeDegree

        - **id**: UUID - the ID of AcademicDegreeDegree to update. This is required.
        - **name**: required.
        - **url**: image url. This parameter is required.
    """
    Authorize.jwt_required()
    return academic_degree_degree_service.update(
        db,
        db_obj=academic_degree_degree_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete AcademicDegreeDegree")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete AcademicDegreeDegree

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    academic_degree_degree_service.remove(db, id)
