import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import StaffFunctionCreate, StaffFunctionRead, StaffFunctionUpdate
from services import staff_function_service

router = APIRouter(prefix="/roles", tags=["StaffFunction"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffFunctionRead])
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return staff_function_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=StaffFunctionRead)
async def create(*,
    db: Session = Depends(get_db),
    body: StaffFunctionCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return staff_function_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffFunctionRead)
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return staff_function_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffFunctionRead)
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: StaffFunctionUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return staff_function_service.update(db, db_obj=staff_function_service.get_by_id(db, id), obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())])
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    staff_function_service.remove(db, id)
