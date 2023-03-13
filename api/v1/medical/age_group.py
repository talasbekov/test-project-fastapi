import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.medical import AgeGroupCreate,AgeGroupUpdate,AgeGroupRead
from services.medical import age_group_service

router = APIRouter(prefix="/age_group", tags=["AgeGroup"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AgeGroupRead],
            summary="Get all AgeGroup")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all AgeGroup

        - **skip**: int - The number of AgeGroup to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of AgeGroup to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return age_group_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=AgeGroupRead,
             summary="Create AgeGroup")
async def create(*,
    db: Session = Depends(get_db),
    body: AgeGroupCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new AgeGroup

        - **head_circumference**: int
        - **shoe_size**: int
        - **neck_circumference**: int
        - **shape_size**: int
        - **bust_size**: int
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return age_group_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AgeGroupRead,
            summary="Get AgeGroup by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Anthropometric Data by id
        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return age_group_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AgeGroupRead,
            summary="Update AgeGroup")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: AgeGroupUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update AgeGroup

        - **id**: UUID - the ID of AgeGroup to update. This is required.
        - **head_circumference**: int
        - **shoe_size**: int
        - **neck_circumference**: int
        - **shape_size**: int
        - **bust_size**: int
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return age_group_service.update(
        db,
        db_obj=age_group_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete AgeGroup")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete AgeGroup
        - **id**: UUId - required
    """
    Authorize.jwt_required()
    age_group_service.remove(db, id)
