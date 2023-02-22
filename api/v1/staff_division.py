import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (StaffDivisionCreate, StaffDivisionRead,
                     StaffDivisionUpdate, UserRead)
from services import staff_division_service

router = APIRouter(prefix="/groups", tags=["StaffDivision"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffDivisionRead])
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return staff_division_service.get_departments(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=StaffDivisionRead)
async def create(*,
    db: Session = Depends(get_db),
    body: StaffDivisionCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return staff_division_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffDivisionRead)
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return staff_division_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffDivisionRead)
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: StaffDivisionUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return staff_division_service.update(db, db_obj=staff_division_service.get_by_id(db, id), obj_in=body)


@router.patch("/{id}/", status_code=status.HTTP_202_ACCEPTED,
              dependencies=[Depends(HTTPBearer())],
              response_model=StaffDivisionRead)
async def update_parent(*,
     db: Session = Depends(get_db),
     id: uuid.UUID,
     new_parent_group_id: uuid.UUID,
     Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return staff_division_service.change_parent_group(db, id, new_parent_group_id)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())])
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authrorize: AuthJWT = Depends()
):
    Authrorize.jwt_required()
    staff_division_service.remove(db, id)
