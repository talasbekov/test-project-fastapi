import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.education import (LanguageCreate,
                               LanguageRead,
                               LanguageUpdate)
from services.education import language_service

router = APIRouter(prefix="/languages",
                   tags=["Languages"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[LanguageRead],
            summary="Get all Languages")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Languages

        - **skip**: int - The number of Languages to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of Languages to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return language_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=LanguageRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: LanguageCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new Language

        - **name**: required
    """
    Authorize.jwt_required()
    return language_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=LanguageRead,
            summary="Get Language by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Language by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return language_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=LanguageRead,
            summary="Update Language")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: LanguageUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Language

        - **id**: UUID - the ID of Language to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return language_service.update(
        db,
        db_obj=language_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Language")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Language

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    language_service.remove(db, id)
