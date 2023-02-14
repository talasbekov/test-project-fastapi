import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import RoleCreate, RoleRead, RoleUpdate
from services import role_service

router = APIRouter(prefix="/roles", tags=["Roles"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[RoleRead])
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return role_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=RoleRead)
async def create(*,
    db: Session = Depends(get_db),
    body: RoleCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return role_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=RoleRead)
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return role_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=RoleRead)
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: RoleUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return role_service.update(db, db_obj=role_service.get_by_id(db, id), obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_202_ACCEPTED,
               dependencies=[Depends(HTTPBearer())],
               response_model=RoleRead)
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    role_service.remove(db, id)
