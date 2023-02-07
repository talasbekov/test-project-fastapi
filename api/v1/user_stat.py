from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import UserStatCreate, UserStatUpdate, UserStatRead
from services import user_stat_service

router = APIRouter(prefix="/user-stats", tags=["UserStats"])


@router.get("", response_model=UserStatRead, dependencies=[Depends(HTTPBearer())])
async def get_all(*,
                  # This is essential for every api we will be writing
                  # This will start our Transaction and will guide us around all service methods
                  db: Session = Depends(get_db),
                  # This block will determine whether or not should this api be secured
                  # To fully secure this api you should invoke method jwt_required()
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    # This will secure our api
    Authorize.jwt_required()
    return user_stat_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserStatRead,
             dependencies=[Depends(HTTPBearer())])
async def create(*,
                 db: Session = Depends(get_db),
                 body: UserStatCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    Authorize.jwt_required()
    return user_stat_service.create(db, body)


@router.put("/{id}/", response_model=UserStatRead, dependencies=[Depends(HTTPBearer())])
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: UserStatUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    Authorize.jwt_required()
    return user_stat_service.update(
        db=db,
        db_obj=user_stat_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_202_ACCEPTED, response_model=UserStatRead,
               dependencies=[Depends(HTTPBearer())])
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    Authorize.jwt_required()
    user_stat_service.remove(db, id)
