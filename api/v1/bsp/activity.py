import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import (ActivityRead,
                     ActivityUpdate,
                     ActivityCreate,)

from services import activity_service


router = APIRouter(prefix="/activity",
                   tags=["Activity"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ActivityRead],
            summary="Get all Activity")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Activity

    - **skip**: int - The number of Activity
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of Activity
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return activity_service.get_all(db, skip, limit)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ActivityRead,
            summary="Get Activity by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Activity by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return activity_service.get_by_id(db, str(id))

@router.post("/", dependencies=[Depends(HTTPBearer())],
            response_model=ActivityRead,
            summary="Create Activity")
async def create(*,
                 db: Session = Depends(get_db),
                 body: ActivityCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Activity

    """
    Authorize.jwt_required()
    return activity_service.create(db, obj_in=body)

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ActivityRead,
            summary="Update Activity")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: ActivityUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Activity

    """
    Authorize.jwt_required()
    return activity_service.update(
        db,
        db_obj=activity_service.get_by_id(db, str(id)),
        obj_in=body)

@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ActivityRead,
            summary="Delete Activity")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Activity

    """
    Authorize.jwt_required()
    return activity_service.remove(db, id)
