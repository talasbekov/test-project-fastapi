import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import BadgeCreate, BadgeRead, BadgeUpdate
from services import badge_service

router = APIRouter(prefix="/badges", tags=["Badges"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[BadgeRead],
            summary="Get all Badges")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all Badges

        - **skip**: int - The number of badges to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of badges to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return badge_service.get_multi(db, skip, limit)

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
    return badge_service.create(db, body)

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BadgeRead,
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
    return badge_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BadgeRead,
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
    return badge_service.update(
        db,
        db_obj=badge_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_204_NO_CONTENT,
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
    badge_service.remove(db, id)


@router.get("/help")
async def help(*,
    db: Session = Depends(get_db)):
    badge_service.add_badge(db, BadgeCreate(name="test", url="sad"))
    raise Exception('help')
