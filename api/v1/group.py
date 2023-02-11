import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import GroupCreate, GroupUpdate, GroupRead, UserRead
from services import group_service

router = APIRouter(prefix="/groups", tags=["Groups"], dependencies=[Depends(HTTPBearer())])


@router.get("", response_model=List[GroupRead])
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return group_service.get_departments(db, skip, limit)


@router.post("", response_model=GroupRead)
async def create(*,
    db: Session = Depends(get_db),
    body: GroupCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return group_service.create(db, body)


@router.get("/{id}/", response_model=GroupRead)
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return group_service.get_by_id(db, id)


@router.put("/{id}/", response_model=GroupRead)
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: GroupUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return group_service.update(db, db_obj=group_service.get_by_id(db, id), obj_in=body)


@router.patch("/{id}/", response_model=GroupRead)
async def update_parent(*,
     db: Session = Depends(get_db),
     id: uuid.UUID,
     new_parent_group_id: uuid.UUID,
     Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return group_service.change_parent_group(db, id, new_parent_group_id)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authrorize: AuthJWT = Depends()
):
    Authrorize.jwt_required()
    group_service.remove(db, id)
