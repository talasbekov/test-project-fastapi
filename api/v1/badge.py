import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import BadgeCreate, BadgeRead, BadgeUpdate, BadgeTypeRead
from services import badge_service

router = APIRouter(
    prefix="/badges",
    tags=["Badges"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[BadgeTypeRead],
            summary="Get all Badges")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Badges

    - **skip**: int - The number of badges to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of badges to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return badge_service.get_multiple(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=BadgeRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: BadgeCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new badge

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return badge_service.create_badge(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BadgeTypeRead,
            summary="Get Badge by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get badge by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return badge_service.get_badge_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BadgeTypeRead,
            summary="Update Badge")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: BadgeUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update badge

        - **id**: UUID - the ID of badge to update. This is required.
        - **name**: required.
        - **url**: image url. This parameter is required.
    """
    Authorize.jwt_required()
    return badge_service.update_badge(db, id, body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Badge")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete badge

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    badge_service.delete_badge(db, id)


@router.get('/black-beret', dependencies=[Depends(HTTPBearer())])
async def black_beret(*,
                      db: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()
                      ):
    """
        Get black beret badge
    """
    Authorize.jwt_required()
    return badge_service.get_black_beret(db)
