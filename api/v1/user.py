import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from models import  User
from schemas import UserCreate, UserUpdate, UserRead
from services import user_service

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(HTTPBearer())])


@router.get("", response_model=List[UserRead])
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return user_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def create(*,
    db: Session = Depends(get_db),
    body: UserCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.create(db, body)


@router.put("/{id}/", response_model=UserRead)
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: UserUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.update(
        db=db,
        db_obj=user_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_202_ACCEPTED, response_model=UserRead)
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_service.remove(db, id)


@router.patch("/{id}/group", response_model=UserRead)
async def update_user_group(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    group_id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.update_user_group(db, id, group_id)


@router.get('/{id}/', response_model=UserRead)
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.get_by_id(db, id)


@router.get('/fields')
async def get_fields(*,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.get_fields()
