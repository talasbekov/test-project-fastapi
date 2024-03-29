import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import ViolationCreate, ViolationRead, ViolationUpdate
from services import violation_service, profile_service

router = APIRouter(
    prefix="/violation",
    tags=["Violation"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ViolationRead],
            summary="Get all Polygraph Check")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Abroad Travel

    - **skip**: int - The number of abroad travel to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of abroad travel to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject()
    return violation_service.get_multi_by_user_id(db, credentials, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ViolationRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: ViolationCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new abroad travel

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return violation_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ViolationRead,
            summary="Update Abroad Travel by id")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: ViolationUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update abroad travel by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    abroad_travel = violation_service.get_by_id(db, str(id))
    return violation_service.update(db=db, db_obj=abroad_travel, obj_in=body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               response_model=ViolationRead,
               summary="Delete Abroad Travel by id")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete abroad travel by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    abroad_travel = violation_service.get_by_id(db, str(id))
    return violation_service.remove(db=db, id=abroad_travel.id)
