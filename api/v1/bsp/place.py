import uuid
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import (PlaceRead,
                     PlaceUpdate,
                     PlaceCreate,)

from services import place_service


router = APIRouter(prefix="/place",
                   tags=["Place"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[PlaceRead],
            summary="Get all Places")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Places

    - **skip**: int - The number of Place
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of Place
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return place_service.get_multi(db, skip, limit)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PlaceRead,
            summary="Get Place by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Place by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return place_service.get_by_id(db, id)

@router.post("/", dependencies=[Depends(HTTPBearer())],
            response_model=PlaceRead,
            summary="Create Place")
async def create(*,
                 db: Session = Depends(get_db),
                 body: PlaceCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Place

    """
    Authorize.jwt_required()
    return place_service.create(db, obj_in=body)

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PlaceRead,
            summary="Update Place")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: PlaceUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Place

    """
    Authorize.jwt_required()
    return place_service.update(
        db,
        db_obj=place_service.get_by_id(db, id),
        obj_in=body)

@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PlaceRead,
            summary="Delete Place")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Place

    """
    Authorize.jwt_required()
    return place_service.remove(db, id)
