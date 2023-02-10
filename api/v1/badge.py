import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import BadgeCreate, BadgeUpdate, BadgeRead
from services import badge_service

router = APIRouter(prefix="/badges", tags=["Badges"], dependencies=[Depends(HTTPBearer())])


@router.get("", response_model=List[BadgeRead])
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return badge_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BadgeRead)
async def create(*,
    db: Session = Depends(get_db),
    body: BadgeCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return badge_service.create(db, body)


@router.get("/{id}/", response_model=BadgeRead)
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return badge_service.get_by_id(db, id)


@router.put("/{id}/", response_model=BadgeRead)
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: BadgeUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return badge_service.update(
        db,
        db_obj=badge_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/",status_code=status.HTTP_202_ACCEPTED)
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    badge_service.remove(db, id)
