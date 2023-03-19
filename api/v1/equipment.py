import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import EquipmentCreate, EquipmentUpdate, EquipmentRead
from services import equipment_service

router = APIRouter(prefix="/equipments", tags=["Equipments"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[EquipmentRead],
            summary="Get all Equipments")
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    """
        Get all Equipments

        - **skip**: int - The number of equipments to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of equipments to return in the response. This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return equipment_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=EquipmentRead,
             summary="Create Equipment")
async def create(*,
    db: Session = Depends(get_db),
    body: EquipmentCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create Equipment

        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return equipment_service.create(db, body)

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=EquipmentRead,
            summary="Get Equipment by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
       Get Equipment by id

       - **id**: UUID - required
    """
    Authorize.jwt_required()
    return equipment_service.get_by_id(db, id)
    

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=EquipmentRead,
            summary="Update Equipment")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: EquipmentUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update Equipment

        - **id**: UUID - the id of equipment to update. This parameter is required
        - **name**: required
        - **quantity**: required
    """
    Authorize.jwt_required()
    return equipment_service.update(
        db=db,
        db_obj=equipment_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Equipment")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete Equipment

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    equipment_service.remove(db, id)
