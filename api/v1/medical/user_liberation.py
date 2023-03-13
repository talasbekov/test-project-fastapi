import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.medical import UserLiberationsRead,UserLiberationsCreate,UserLiberationsUpdate
from services.medical import user_liberations_service

router = APIRouter(prefix="/user_liberations", tags=["UserLiberations"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[UserLiberationsRead],
            summary="Get all UserLiberations")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all UserLiberations

        - **skip**: int - The number of UserLiberations to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of UserLiberations to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return user_liberations_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=UserLiberationsRead,
             summary="Create UserLiberations")
async def create(*,
    db: Session = Depends(get_db),
    body: UserLiberationsCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create new UserLiberations

        - **reason**: str
        - **liberation_name**: str
        - **initiator**: str
        - **start_date**: datetime.datetime
        - **end_date**: datetime.datetime
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return user_liberations_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=UserLiberationsRead,
            summary="Get UserLiberations by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get UserLiberations by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return user_liberations_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model= UserLiberationsRead,
            summary="Update UserLiberations")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: UserLiberationsUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update UserLiberations

        - **id**: UUID - the ID of UserLiberations to update. This is required.
        - **reason**: str
        - **liberation_name**: str
        - **initiator**: str
        - **start_date**: datetime.datetime
        - **end_date**: datetime.datetime
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return user_liberations_service.update(
        db,
        db_obj=user_liberations_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete UserLiberations")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete a UserLiberations

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    user_liberations_service.remove(db, id)
