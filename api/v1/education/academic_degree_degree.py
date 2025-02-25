import uuid
from typing import List
from sqlalchemy.exc import DatabaseError
from models.education import AcademicDegreeDegree
from sqlalchemy import func
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (AcademicDegreeDegreeCreate,
                               AcademicDegreeDegreeRead,
                               AcademicDegreeDegreeUpdate,
                               AcademicDegreeDegreeReadPagination)
from services.education import academic_degree_degree_service

router = APIRouter(prefix="/academic_degree_degrees",
                   tags=["AcademicDegreeDegrees"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=AcademicDegreeDegreeReadPagination,
            summary="Get all AcademicDegreeDegrees")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  filter: str = '',
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all AcademicDegreeDegrees

    - **skip**: int - The number of AcademicDegreeDegrees
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of AcademicDegreeDegrees
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return academic_degree_degree_service.get_all(db, skip, limit, filter)


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
    """
    Authorize.jwt_required()
    return academic_degree_degree_service.create(db, body)

@router.get("/check/")
async def check(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    filter: str = '',
    Authorize: AuthJWT = Depends()
):
    try:
        academic_degree_degrees = db.query(AcademicDegreeDegree)\
            .order_by(func.to_char(AcademicDegreeDegree.name))\
            .offset(skip)\
            .limit(limit)\
            .all()
        return {"data": academic_degree_degrees}
    except DatabaseError as e:
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while querying the database.")

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AcademicDegreeDegreeRead,
            summary="Get AcademicDegreeDegree by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get AcademicDegreeDegree by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return academic_degree_degree_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AcademicDegreeDegreeRead,
            summary="Update AcademicDegreeDegree")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: AcademicDegreeDegreeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update AcademicDegreeDegree

        - **id**: UUID - the ID of AcademicDegreeDegree to update.
            This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return academic_degree_degree_service.update(
        db,
        db_obj=academic_degree_degree_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete AcademicDegreeDegree")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete AcademicDegreeDegree

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    academic_degree_degree_service.remove(db, str(id))
