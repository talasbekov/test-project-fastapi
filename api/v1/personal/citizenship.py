import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import CitizenshipCreate, CitizenshipUpdate, CitizenshipRead
from services import citizenship_service


router = APIRouter(
    prefix="/citizenship",
    tags=["Citizenship"],
    dependencies=[
        Depends(
            HTTPBearer())])

@router.get("", dependencies=[Depends(HTTPBearer())],
                response_model=List[CitizenshipRead],
                summary="Get all Citizenship")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Citizenship

        - **skip**: int - The number of Citizenship
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Citizenship
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return citizenship_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
                dependencies=[Depends(HTTPBearer())],
                response_model=CitizenshipRead,
                summary="Create Citizenship")
async def create(*,
                db: Session = Depends(get_db),
                body: CitizenshipCreate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Create new Citizenship
    """
    Authorize.jwt_required()
    return citizenship_service.create(db, body)

@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=CitizenshipRead,
                summary="Get Citizenship by ID")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Citizenship by ID
    """
    Authorize.jwt_required()
    return citizenship_service.get_by_id(db, id)

@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=CitizenshipRead,
                summary="Update Citizenship by ID")
async def update(*,
                db: Session = Depends(get_db),
                id: str,
                body: CitizenshipUpdate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Update Citizenship by ID
    """
    Authorize.jwt_required()
    citizenship = citizenship_service.get_by_id(db, id)
    return citizenship_service.update(db, db_obj=citizenship, obj_in=body)

@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=CitizenshipRead,
                summary="Delete Citizenship by ID")
async def delete(*,
                db: Session = Depends(get_db),
                id: str,
                Authorize: AuthJWT = Depends()
                ):
    """
        Delete Citizenship by ID
    """
    Authorize.jwt_required()
    return citizenship_service.remove(db, id)
