import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (CourseProviderCreate,
                               CourseProviderRead,
                               CourseProviderUpdate,
                               CourseProviderReadPagination)
from services.education import course_provider_service

router = APIRouter(prefix="/course_providers",
                   tags=["CourseProviders"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[CourseProviderReadPagination],
            summary="Get all CourseProviders")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all CourseProviders

    - **skip**: int - The number of CourseProviders
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of CourseProviders
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return course_provider_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=CourseProviderRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: CourseProviderCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new CourseProvider

        - **name**: required
    """
    Authorize.jwt_required()
    return course_provider_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CourseProviderRead,
            summary="Get CourseProvider by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get CourseProvider by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return course_provider_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CourseProviderRead,
            summary="Update CourseProvider")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: CourseProviderUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update CourseProvider

        - **id**: UUID - the ID of CourseProvider to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return course_provider_service.update(
        db,
        db_obj=course_provider_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete CourseProvider")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete CourseProvider

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    course_provider_service.remove(db, str(id))
