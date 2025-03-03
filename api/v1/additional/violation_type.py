import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import ViolationTypeCreate, ViolationTypeUpdate, ViolationTypeRead
from services import violation_type_service


router = APIRouter(
    prefix="/violation_type",
    tags=["ViolationType"],
    dependencies=[
        Depends(
            HTTPBearer())])

@router.get("", dependencies=[Depends(HTTPBearer())],
                response_model=List[ViolationTypeRead],
                summary="Get all ViolationType")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all ViolationType

        - **skip**: int - The number of ViolationType
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of ViolationType
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return violation_type_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
                dependencies=[Depends(HTTPBearer())],
                response_model=ViolationTypeRead,
                summary="Create ViolationType")
async def create(*,
                db: Session = Depends(get_db),
                body: ViolationTypeCreate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Create new ViolationType
    """
    Authorize.jwt_required()
    return violation_type_service.create(db, body)

@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=ViolationTypeRead,
                summary="Get ViolationType by ID")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get ViolationType by ID
    """
    Authorize.jwt_required()
    return violation_type_service.get_by_id(db, id)

@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=ViolationTypeRead,
                summary="Update ViolationType by ID")
async def update(*,
                db: Session = Depends(get_db),
                id: str,
                body: ViolationTypeUpdate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Update ViolationType by ID
    """
    Authorize.jwt_required()
    ViolationType = violation_type_service.get_by_id(db, id)
    return violation_type_service.update(db, db_obj=ViolationType, obj_in=body)

@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=ViolationTypeRead,
                summary="Delete ViolationType by ID")
async def delete(*,
                db: Session = Depends(get_db),
                id: str,
                Authorize: AuthJWT = Depends()
                ):
    """
        Delete ViolationType by ID
    """
    Authorize.jwt_required()
    return violation_type_service.remove(db, id)
