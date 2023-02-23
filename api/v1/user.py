import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import User
from schemas import UserCreate, UserPermission, UserRead, UserUpdate, UserGroupUpdate
from services import user_service

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())], response_model=List[UserRead])
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return user_service.get_multi(db, skip, limit)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())], response_model=UserRead)
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


@router.post("/group", status_code=status.HTTP_202_ACCEPTED,
              dependencies=[Depends(HTTPBearer())],
              response_model=UserRead)
async def update_user_group(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    body: UserGroupUpdate
):
    Authorize.jwt_required()
    return user_service.update_user_group(db, body)


@router.get('/{id}/', dependencies=[Depends(HTTPBearer())],
            response_model=UserRead)
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.get_by_id(db, id)


@router.get('/fields', dependencies=[Depends(HTTPBearer())])
async def get_fields(*,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.get_fields()


@router.post("/add-permission")
def add_permission(*,
    db: Session = Depends(get_db),
    body: UserPermission,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_service.add_permission(db, body)


@router.post("/remove-permission")
def remove_permission(*,
    db: Session = Depends(get_db),
    body: UserPermission,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_service.remove_permission(db, body)
