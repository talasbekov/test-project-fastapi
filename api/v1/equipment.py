from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import EquipmentCreate, EquipmentUpdate, EquipmentRead
from services import equipment_service

router = APIRouter(prefix="/equipments", tags=["Equipments"], dependencies=[Depends(HTTPBearer())])


@router.get("", response_model=List[EquipmentRead], dependencies=[Depends(HTTPBearer())])
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return equipment_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=List[EquipmentRead],
             dependencies=[Depends(HTTPBearer())])
async def create(*,
    db: Session = Depends(get_db),
    body: EquipmentCreate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.create(db, body)


@router.put("/{id}/", response_model=List[EquipmentRead], dependencies=[Depends(HTTPBearer())])
async def update(*,
    db: Session = Depends(get_db),
    id: str,
    body: EquipmentUpdate,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return equipment_service.update(
        db=db,
        db_obj=equipment_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_202_ACCEPTED, response_model=List[EquipmentRead],
               dependencies=[Depends(HTTPBearer())])
async def delete(*,
    db: Session = Depends(get_db),
    id: str,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    equipment_service.remove(db, id)
