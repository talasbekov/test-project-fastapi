from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import UserCreate, UserUpdate, UserRead
from services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserRead], dependencies=[Depends(HTTPBearer())])
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return user_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=List[UserRead],
             dependencies=[Depends(HTTPBearer())])
async def create(*,
    db: Session = Depends(get_db),
    body: UserCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.create(db, body)


@router.put("/{id}/", response_model=List[UserRead], dependencies=[Depends(HTTPBearer())])
async def update(*,
    db: Session = Depends(get_db),
    id: str,
    body: UserUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.update(
        db=db,
        db_obj=user_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_202_ACCEPTED, response_model=List[UserRead],
               dependencies=[Depends(HTTPBearer())])
async def delete(*,
    db: Session = Depends(get_db),
    id: str,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_service.remove(db, id)
