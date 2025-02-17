import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import IllnessTypeCreate, IllnessTypeUpdate, IllnessTypeRead
from services import illness_type_service


router = APIRouter(
    prefix="/illness_type",
    tags=["IllnessType"],
    dependencies=[
        Depends(
            HTTPBearer())])

@router.get("", dependencies=[Depends(HTTPBearer())],
                response_model=List[IllnessTypeRead],
                summary="Get all IllnessType")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all IllnessType

        - **skip**: int - The number of IllnessType
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of IllnessType
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return illness_type_service.get_multi(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
                dependencies=[Depends(HTTPBearer())],
                response_model=IllnessTypeRead,
                summary="Create IllnessType")
async def create(*,
                db: Session = Depends(get_db),
                body: IllnessTypeCreate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Create new IllnessType
    """
    Authorize.jwt_required()
    return illness_type_service.create(db, body)

@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=IllnessTypeRead,
                summary="Get IllnessType by ID")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get IllnessType by ID
    """
    Authorize.jwt_required()
    return illness_type_service.get_by_id(db, id)

@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=IllnessTypeRead,
                summary="Update IllnessType by ID")
async def update(*,
                db: Session = Depends(get_db),
                id: str,
                body: IllnessTypeUpdate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Update IllnessType by ID
    """
    Authorize.jwt_required()
    IllnessType = illness_type_service.get_by_id(db, id)
    return illness_type_service.update(db, db_obj=IllnessType, obj_in=body)

@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=IllnessTypeRead,
                summary="Delete IllnessType by ID")
async def delete(*,
                db: Session = Depends(get_db),
                id: str,
                Authorize: AuthJWT = Depends()
                ):
    """
        Delete IllnessType by ID
    """
    Authorize.jwt_required()
    return illness_type_service.remove(db, id)
