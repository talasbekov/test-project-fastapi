import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import UserStatCreate, UserStatUpdate, UserStatRead
from services import user_stat_service, user_service

router = APIRouter(prefix="/user-stats", tags=["UserStats"], dependencies=[Depends(HTTPBearer())])


@router.get("", response_model=List[UserStatRead], dependencies=[Depends(HTTPBearer())],
            summary="Get all UserStats")
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    """
        Get all UserStats

       - **skip**: int - The number of UserStats to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of UserStats to return in the response. This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return user_stat_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=UserStatRead,
             summary="Create UserStat")
async def create(*,
    db: Session = Depends(get_db),
    body: UserStatCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create UserStat

        - **user_id**: UUID - the ID of the user. This parameter is required and should exist in database.
        - **physical_training**: int - representing the user's physical training score.
        - **fire_training**: int - representing the user's fire training score.
        - **attendance**: int - representing the user's attendance score.
        - **activity**: int - representing the user's activity score.
        - **opinion_of_colleagues**: int - representing the user's opinion of colleagues score.
        - **opinion_of_management**: int - representing the user's opinion of management score.
    """
    Authorize.jwt_required()
    return user_stat_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=UserStatRead,
            summary="Get UserStat by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get UserStat by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return user_stat_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=UserStatRead,
            summary="Update UserStat")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: UserStatUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update UserStat

        - **id**: UUID - the ID of the UserStat. This is required.
        - **user_id**: UUID - the ID of the user. This parameter is required and should exist in database.
        - **physical_training**: int - representing the user's physical training score. This is required.
        - **fire_training**: int - representing the user's fire training score. This is required.
        - **attendance**: int - representing the user's attendance score. This is required.
        - **activity**: int - representing the user's activity score. This is required.
        - **opinion_of_colleagues**: int - representing the user's opinion of colleagues score. This is required.
        - **opinion_of_management**: int - representing the user's opinion of management score. This is required.
    """
    Authorize.jwt_required()
    user_service.get_by_id(db, body.user_id)
    return user_stat_service.update(
        db=db,
        db_obj=user_stat_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete UserStat")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete UserStat

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    user_stat_service.remove(db, id)
