import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import ActivityTypeCreate, ActivityTypeUpdate, ActivityTypeRead
from services import activity_type_service


router = APIRouter(
    prefix="/activity_type",
    tags=["ActivityType"],
    dependencies=[
        Depends(
            HTTPBearer())])

@router.get("", dependencies=[Depends(HTTPBearer())],
                response_model=List[ActivityTypeRead],
                summary="Get all ActivityType")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all ActivityType

        - **skip**: int - The number of ActivityType
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of ActivityType
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return activity_type_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
                dependencies=[Depends(HTTPBearer())],
                response_model=ActivityTypeRead,
                summary="Create ActivityType")
async def create(*,
                db: Session = Depends(get_db),
                body: ActivityTypeCreate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Create new ActivityType
    """
    Authorize.jwt_required()
    return activity_type_service.create(db, body)

@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=ActivityTypeRead,
                summary="Get ActivityType by ID")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get ActivityType by ID
    """
    Authorize.jwt_required()
    return activity_type_service.get_by_id(db, id)

@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=ActivityTypeRead,
                summary="Update ActivityType by ID")
async def update(*,
                db: Session = Depends(get_db),
                id: str,
                body: ActivityTypeUpdate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Update ActivityType by ID
    """
    Authorize.jwt_required()
    ActivityType = activity_type_service.get_by_id(db, id)
    return activity_type_service.update(db, db_obj=ActivityType, obj_in=body)

@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=ActivityTypeRead,
                summary="Delete ActivityType by ID")
async def delete(*,
                db: Session = Depends(get_db),
                id: str,
                Authorize: AuthJWT = Depends()
                ):
    """
        Delete ActivityType by ID
    """
    Authorize.jwt_required()
    return activity_type_service.remove(db, id)
