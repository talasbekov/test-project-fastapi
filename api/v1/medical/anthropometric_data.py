import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas.medical import (
    AnthropometricDataRead,
    AnthropometricDataCreate,
    AnthropometricDataUpdate
)
from services.medical import anthropometric_data_service

router = APIRouter(
    prefix="/anthropometric_data",
    tags=["AnthropometricData"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AnthropometricDataRead],
            summary="Get all AnthropometricData")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all AnthropometricData

        - **skip**: int - The number of AnthropometricData
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of AnthropometricData
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return anthropometric_data_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=AnthropometricDataRead,
             summary="Create AnthropometricData")
async def create(*,
                 db: Session = Depends(get_db),
                 body: AnthropometricDataCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new AnthropometricData

        - **head_circumference**: int
        - **shoe_size**: int
        - **neck_circumference**: int
        - **shape_size**: int
        - **bust_size**: int
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return anthropometric_data_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AnthropometricDataRead,
            summary="Get AnthropometricData by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Anthropometric Data by id
        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return anthropometric_data_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AnthropometricDataRead,
            summary="Update AnthropometricData")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: AnthropometricDataUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update AnthropometricData

        - **id**: UUID - the ID of AnthropometricData to update. This is required.
        - **head_circumference**: int
        - **shoe_size**: int
        - **neck_circumference**: int
        - **shape_size**: int
        - **bust_size**: int
        - **profile_id**: uuid.UUID
    """
    Authorize.jwt_required()
    return anthropometric_data_service.update(
        db,
        db_obj=anthropometric_data_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete AnthropometricData")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete AnthropometricData
        - **id**: UUId - required
    """
    Authorize.jwt_required()
    anthropometric_data_service.remove(db, str(id))
