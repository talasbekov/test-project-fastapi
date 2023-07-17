import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import (AbsentUserRead,
                     AbsentUserUpdate,
                     AbsentUserCreate,)

from services import absent_user_service


router = APIRouter(prefix="/absent_user",
                   tags=["AbsentUser"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AbsentUserRead],
            summary="Get all Absent User")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all AbsentUser

    - **skip**: int - The number of AbsentUser
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of AbsentUser
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return absent_user_service.get_multi(db, skip, limit)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AbsentUserRead,
            summary="Get AbsentUser by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get AbsentUser by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return absent_user_service.get_by_id(db, id)

@router.post("/", dependencies=[Depends(HTTPBearer())],
            response_model=AbsentUserRead,
            summary="Create AbsentUser")
async def create(*,
                 db: Session = Depends(get_db),
                 body: AbsentUserCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create AbsentUser

    """
    Authorize.jwt_required()
    return absent_user_service.create(db, obj_in=body)

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AbsentUserRead,
            summary="Update AbsentUser")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: AbsentUserUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update AbsentUser

    """
    Authorize.jwt_required()
    return absent_user_service.update(
        db,
        db_obj=absent_user_service.get_by_id(db, id),
        obj_in=body)

@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AbsentUserRead,
            summary="Delete AbsentUser")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete AbsentUser

    """
    Authorize.jwt_required()
    return absent_user_service.remove(db, id)
