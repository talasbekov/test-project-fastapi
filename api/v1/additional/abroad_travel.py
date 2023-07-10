import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import AbroadTravelCreate, AbroadTravelRead, AbroadTravelUpdate
from services import abroad_travel_service, profile_service

router = APIRouter(
    prefix="/abroad-travel",
    tags=["Abroad Travel"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AbroadTravelRead],
            summary="Get all Abroad Travel")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Abroad Travel

    - **skip**: int - The number of abroad travel to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of abroad travel to return in the response.
        This parameter is optional and defaults to 100.

    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject()
    return abroad_travel_service.get_multi_by_user_id(
        db, credentials, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=AbroadTravelRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: AbroadTravelCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new abroad travel

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    profile = profile_service.get_by_user_id(db, user_id)
    body.profile_id = profile.id
    return abroad_travel_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AbroadTravelRead,
            summary="Update Abroad Travel by id")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: AbroadTravelUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update abroad travel by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    abroad_travel = abroad_travel_service.get_by_id(db, id)
    return abroad_travel_service.update(db, abroad_travel, body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               response_model=AbroadTravelRead,
               summary="Delete Abroad Travel by id")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete abroad travel by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    abroad_travel = abroad_travel_service.get_by_id(db, id)
    return abroad_travel_service.delete(db, abroad_travel)
