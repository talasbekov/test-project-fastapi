import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import StaffUnitCreate, StaffUnitRead, StaffUnitUpdate
from services import rank_service, staff_unit_service

router = APIRouter(prefix="/positions", tags=["StaffUnit"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffUnitRead])
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return staff_unit_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=StaffUnitRead)
async def create(*,
    db: Session = Depends(get_db),
    body: StaffUnitCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return staff_unit_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffUnitRead)
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: StaffUnitUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    rank_service.get_by_id(db, body.max_rank_id)
    return staff_unit_service.update(
        db=db,
        db_obj=staff_unit_service.get_by_id(db, id),
        obj_in=body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffUnitRead)
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return staff_unit_service.get_by_id(db, id)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())])
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    staff_unit_service.remove(db, id)
