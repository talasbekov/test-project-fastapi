import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import PolygraphCheckCreate, PolygraphCheckRead, PolygraphCheckUpdate
from services import polyhraph_check_service

router = APIRouter(
    prefix="/polygraph-check",
    tags=["Polygraph Check"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[PolygraphCheckRead],
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
    return polyhraph_check_service.get_multi_by_user_id(
        db, credentials, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=PolygraphCheckRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: PolygraphCheckCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new polyhraph_check

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return polyhraph_check_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PolygraphCheckRead,
            summary="Update polyhraph_check by id")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: PolygraphCheckUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update polyhraph_check by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    check = polyhraph_check_service.get_by_id(db, str(id))
    return polyhraph_check_service.update(db, check, body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               response_model=PolygraphCheckRead,
               summary="Delete polyhraph_check by id")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete polyhraph_check by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    polyhraph_check = polyhraph_check_service.get_by_id(db, str(id))
    return polyhraph_check_service.remove(db=db, id=polyhraph_check.id)
