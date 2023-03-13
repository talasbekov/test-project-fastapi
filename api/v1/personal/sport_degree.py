import uuid

from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import SportDegreeCreate, SportDegreeUpdate, SportDegreeRead
from services import sport_degree_service

router = APIRouter(prefix="/sport_degree", tags=["SportDegree"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[SportDegreeRead],
            summary="Get all SportDegree")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all SportDegree

        - **skip**: int - The number of SportDegree to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of SportDegree to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return sport_degree_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=SportDegreeRead,
             summary="Create SportDegree")
async def create(*,
    db: Session = Depends(get_db),
    body: SportDegreeCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new SportDegree

        - **name**: str
        - **assignment_date**: datetime.date
        - **document_link**: str
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return sport_degree_service.create(db, body)

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SportDegreeRead,
            summary="Get SportDegree by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get SportDegree by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return sport_degree_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SportDegreeRead,
            summary="Update SportDegree")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: SportDegreeUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update SportDegree

        - **id**: UUID - the ID of SportDegree to update. This is required.
        - **name**: str
        - **assignment_date**: datetime.date
        - **document_link**: str
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return sport_degree_service.update(
        db,
        db_obj=sport_degree_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete SportDegree")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete SportDegree

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    sport_degree_service.remove(db, id)
