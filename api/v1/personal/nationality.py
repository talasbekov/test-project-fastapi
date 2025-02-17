import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import NationalityCreate, NationalityUpdate, NationalityRead
from services import nationality_service


router = APIRouter(
    prefix="/nationality",
    tags=["Nationality"],
    dependencies=[
        Depends(
            HTTPBearer())])

@router.get("", dependencies=[Depends(HTTPBearer())],
                response_model=List[NationalityRead],
                summary="Get all Nationality")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Nationality

        - **skip**: int - The number of Nationality
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Nationality
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return nationality_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
                dependencies=[Depends(HTTPBearer())],
                response_model=NationalityRead,
                summary="Create Nationality")
async def create(*,
                db: Session = Depends(get_db),
                body: NationalityCreate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Create new Nationality
    """
    Authorize.jwt_required()
    return nationality_service.create(db, body)

@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=NationalityRead,
                summary="Get Nationality by ID")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Nationality by ID
    """
    Authorize.jwt_required()
    return nationality_service.get_by_id(db, id)

@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=NationalityRead,
                summary="Update Nationality by ID")
async def update(*,
                db: Session = Depends(get_db),
                id: str,
                body: NationalityUpdate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Update Nationality by ID
    """
    Authorize.jwt_required()
    nationality = nationality_service.get_by_id(db, id)
    return nationality_service.update(db, db_obj=nationality, obj_in=body)

@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=NationalityRead,
                summary="Delete Nationality by ID")
async def delete(*,
                db: Session = Depends(get_db),
                id: str,
                Authorize: AuthJWT = Depends()
                ):
    """
        Delete Nationality by ID
    """
    Authorize.jwt_required()
    return nationality_service.remove(db, id)
