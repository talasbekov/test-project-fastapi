import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import FamilyCreate, FamilyRead, FamilyUpdate
from services import family_service

router = APIRouter(
    prefix="/families",
    tags=["Family Members"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[FamilyRead])
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    Authorize.jwt_required()
    return family_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=FamilyRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: FamilyCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    Authorize.jwt_required()
    return family_service.create(db, obj_in=body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=FamilyRead)
async def get(*,
              db: Session = Depends(get_db),
              id: uuid.UUID,
              Authorize: AuthJWT = Depends()
              ):
    Authorize.jwt_required()
    return family_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=FamilyRead)
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: FamilyUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    Authorize.jwt_required()
    return family_service.update(
        db, db_obj=family_service.get_by_id(db, str(id)), obj_in=body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    Authorize.jwt_required()
    return family_service.remove(db, str(id))
