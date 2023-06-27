import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import SportAchievementCreate, SportAchievementUpdate, SportAchievementRead
from services import sport_achievement_service

router = APIRouter(
    prefix="/sport_achievement",
    tags=["SportAchievement"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[SportAchievementRead],
            summary="Get all SportAchievement")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all SportAchievement

        - **skip**: int - The number of SportAchievement
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of SportAchievement
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return sport_achievement_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=SportAchievementRead,
             summary="Create SportAchievement")
async def create(*,
                 db: Session = Depends(get_db),
                 body: SportAchievementCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new SportAchievement

        - **name**: str
        - **assignment_date**: datetime.date
        - **document_link**: str
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return sport_achievement_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SportAchievementRead,
            summary="Get SportAchievement by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get SportAchievement by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return sport_achievement_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SportAchievementRead,
            summary="Update SportAchievement")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: SportAchievementUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update SportAchievement

        - **id**: UUID - the ID of SportAchievement to update. This is required.
        - **name**: str
        - **assignment_date**: datetime.date
        - **document_link**: str
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return sport_achievement_service.update(
        db,
        db_obj=sport_achievement_service.get_by_id(db, id),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete SportAchievement")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete SportAchievement

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    sport_achievement_service.remove(db, id)
