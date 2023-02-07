from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import PositionCreate, PositionUpdate, PositionRead
from services import position_service

router = APIRouter(prefix="/positions", tags=["Positions"])


@router.get("", response_model=PositionRead, dependencies=[Depends(HTTPBearer())])
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return position_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PositionRead,
             dependencies=[Depends(HTTPBearer())])
async def create(*,
    db: Session = Depends(get_db),
    body: PositionCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return position_service.create(db, body)


@router.put("/{id}/", response_model=PositionRead, dependencies=[Depends(HTTPBearer())])
async def update(*,
    db: Session = Depends(get_db),
    id: str,
    body: PositionUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return position_service.update(
        db=db,
        db_obj=position_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_202_ACCEPTED, response_model=PositionRead,
               dependencies=[Depends(HTTPBearer())])
async def delete(*,
    db: Session = Depends(get_db),
    id: str,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    position_service.remove(db, id)
