import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import RankCreate, RankUpdate, RankRead
from services import rank_service

router = APIRouter(
    prefix="/ranks",
    tags=["Ranks"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[RankRead],
            summary="Get all Ranks")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Ranks

       - **skip**: int - The number of ranks
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ranks
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return rank_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=RankRead,
             summary="Create Rank")
async def create(*,
                 db: Session = Depends(get_db),
                 body: RankCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Rank

        - **name**: required
    """
    Authorize.jwt_required()
    return rank_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=RankRead,
            summary="Get Rank by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Rank by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return rank_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=RankRead,
            summary="Update Rank")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: RankUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Rank

        - **id**: UUID - the ID of badge to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    return rank_service.update(
        db,
        db_obj=rank_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Rank")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Rank

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    rank_service.remove(db, str(id))
