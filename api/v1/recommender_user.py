import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (
    RecommenderUserCreate,
    RecommenderUserUpdate,
    RecommenderUserRead
)
from services import recommender_user_service

router = APIRouter(
    prefix="/recommender_users",
    tags=["Recommender Users"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[RecommenderUserRead],
            summary="Get all Recommender Users")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Recommender Users

       - **skip**: int - The number of ranks
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of ranks
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return recommender_user_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=RecommenderUserRead,
             summary="Create Recommender User")
async def create(*,
                 db: Session = Depends(get_db),
                 body: RecommenderUserCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Recommender User

    """
    Authorize.jwt_required()
    return recommender_user_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=RecommenderUserRead,
            summary="Get Recommender User by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Recommender User by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return recommender_user_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=RecommenderUserRead,
            summary="Update Recommender User")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: RecommenderUserUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Recommender User

        - **id**: UUID - the ID of badge to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    recommender_user = recommender_user_service.get_by_id(db, str(id))
    return recommender_user_service.update(
        db, db_obj=recommender_user, obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Recommender User")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Recommender User

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    recommender_user_service.remove(db, str(id))
