import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.medical import (
    UserLiberationRead,
    UserLiberationCreate,
    UserLiberationUpdate
)
from services.medical import user_liberations_service

router = APIRouter(
    prefix="/user_liberations",
    tags=["UserLiberation"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[UserLiberationRead],
            summary="Get all UserLiberation")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all UserLiberation

    - **skip**: int - The number of UserLiberation
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of UserLiberation
        to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return user_liberations_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=UserLiberationRead,
             summary="Create UserLiberation")
async def create(*,
                 db: Session = Depends(get_db),
                 body: UserLiberationCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new UserLiberation

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
            response_model=UserLiberationRead,
            summary="Get UserLiberation by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get UserLiberation by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return user_liberations_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=UserLiberationRead,
            summary="Update UserLiberation")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: UserLiberationUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update UserLiberation

        - **id**: UUID - the ID of UserLiberation to update. This is required.
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
        db_obj=user_liberations_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete UserLiberation")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete a UserLiberation

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    user_liberations_service.remove(db, str(id))
