import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import (PsychologicalCheckCreate,
                     PsychologicalCheckRead,
                     PsychologicalCheckUpdate)

from services import psychological_check_service

router = APIRouter(prefix="/psychological-check",
                   tags=["Psychological Check"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[PsychologicalCheckRead],
            summary="Get all psychological check")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all psychological check

    - **skip**: int - The number of psychological check to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of psychological check to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject()
    return psychological_check_service.get_multi_by_user_id(
        db, credentials, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=PsychologicalCheckRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: PsychologicalCheckCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new psychological check

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return psychological_check_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PsychologicalCheckRead,
            summary="Update psychological check by id")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: PsychologicalCheckUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update psychological check by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    check = psychological_check_service.get_by_id(db, str(id))
    return psychological_check_service.update(db, check, body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               response_model=PsychologicalCheckRead,
               summary="Delete psychological check by id")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete psychological check by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    psychological_check = psychological_check_service.get_by_id(db, str(id))
    return psychological_check_service.remove(db=db, id=psychological_check.id)
