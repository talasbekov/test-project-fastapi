import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import UserOathCreate, UserOathRead, UserOathUpdate
from services import user_oath_service

router = APIRouter(
    prefix="/user_oaths",
    tags=["UserOath"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[UserOathRead],
            summary="Get all User Oaths")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    """
       Get all User Oaths

       - **skip**: int - The number of User Oaths to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of User Oaths to return in the response. This parameter is optional and defaults to 10.
   """
    Authorize.jwt_required()
    return user_oath_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=UserOathRead,
             summary="Create User Oath")
async def create(*,
                 db: Session = Depends(get_db),
                 body: UserOathCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create User Oath

        **date** - required - datetime
        **user_id** - required - uuid
        **military_unit_id** - required - uuid

    """
    Authorize.jwt_required()
    return user_oath_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=UserOathRead,
            summary="Update User Oath")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: UserOathUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update User Oath

        **date** - required - datetime
        **user_id** - required - uuid
        **military_unit_id** - required - uuid
    """
    Authorize.jwt_required()
    return user_oath_service.update(
        db=db,
        db_obj=user_oath_service.get_by_id(db, id),
        obj_in=body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=UserOathRead,
            summary="Get User Oath by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get User Oath by id

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    return user_oath_service.get_by_id(db, id)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete User Oath")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete User Oath

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    user_oath_service.remove(db, id)
