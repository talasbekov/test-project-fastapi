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


@router.get("help")
async def help(
    db: Session = Depends(get_db),
):
    return user_service.create(db, UserCreate(email="user@example.com", password="password",
                                              group_id=uuid.uuid4(),
                                              position_id=uuid.uuid4(),
                                              call_sign='calla1234',
                                              id_number='142351521',
                                              last_name='last',
                                              first_name='first'))



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


@router.patch("/{id}/group", status_code=status.HTTP_202_ACCEPTED,
              dependencies=[Depends(HTTPBearer())],
              response_model=UserRead)
async def update_user_group(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    group_id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.update_user_group(db, id, group_id)


@router.get('/{id}/', dependencies=[Depends(HTTPBearer())],
            response_model=UserRead)
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.get_by_id(db, id)


@router.get('/fields', dependencies=[Depends(HTTPBearer())],)
async def get_fields(*,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.get_fields()
