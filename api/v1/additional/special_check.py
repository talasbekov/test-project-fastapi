import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import SpecialCheckCreate, SpecialCheckRead, SpecialCheckUpdate
from services import special_check_service, profile_service

router = APIRouter(
    prefix="/special-check",
    tags=["Special Check"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[SpecialCheckRead],
            summary="Get all Polygraph Check")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all special_check

    - **skip**: int - The number of special_check to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of special_check to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject()
    return special_check_service.get_multi_by_user_id(
        db, credentials, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=SpecialCheckRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: SpecialCheckCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new special_check

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return special_check_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SpecialCheckRead,
            summary="Update Abroad Travel by id")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: SpecialCheckUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update special_check by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    special_check = special_check_service.get_by_id(db, str(id))
    return special_check_service.update(db=db, db_obj=special_check, obj_in=body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               response_model=SpecialCheckRead,
               summary="Delete special_check by id")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete special_check by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    special_check = special_check_service.get_by_id(db, str(id))
    return special_check_service.remove(db=db, id=special_check.id)
