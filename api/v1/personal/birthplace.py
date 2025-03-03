import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import BirthplaceCreate, BirthplaceUpdate, BirthplaceRead
from services import birthplace_service


router = APIRouter(
    prefix="/birthplace",
    tags=["Birthplace"],
    dependencies=[
        Depends(
            HTTPBearer())])

@router.get("", dependencies=[Depends(HTTPBearer())],
                response_model=List[BirthplaceRead],
                summary="Get all Birthplace")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Birthplace

        - **skip**: int - The number of Birthplace
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Birthplace
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return birthplace_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
                dependencies=[Depends(HTTPBearer())],
                response_model=BirthplaceRead,
                summary="Create Birthplace")
async def create(*,
                db: Session = Depends(get_db),
                body: BirthplaceCreate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Create new Birthplace
    """
    Authorize.jwt_required()
    return birthplace_service.create(db, body)

@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=BirthplaceRead,
                summary="Get Birthplace by ID")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Birthplace by ID
    """
    Authorize.jwt_required()
    return birthplace_service.get_by_id(db, id)

@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=BirthplaceRead,
                summary="Update Birthplace by ID")
async def update(*,
                db: Session = Depends(get_db),
                id: str,
                body: BirthplaceUpdate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Update Birthplace by ID
    """
    Authorize.jwt_required()
    Birthplace = birthplace_service.get_by_id(db, id)
    return birthplace_service.update(db, db_obj=Birthplace, obj_in=body)

@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=BirthplaceRead,
                summary="Delete Birthplace by ID")
async def delete(*,
                db: Session = Depends(get_db),
                id: str,
                Authorize: AuthJWT = Depends()
                ):
    """
        Delete Birthplace by ID
    """
    Authorize.jwt_required()
    return birthplace_service.remove(db, id)
