import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import StaffFunctionCreate, StaffFunctionRead, StaffFunctionUpdate
from services import staff_function_service

router = APIRouter(prefix="/staff_function", tags=["StaffFunction"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffFunctionRead],
            summary="Get all Staff Functions")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
       Get all Staff Functions

       - **skip**: int - The number of staff functions to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff functions to return in the response. This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return staff_function_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=StaffFunctionRead,
             summary="Create Staff Function")
async def create(*,
    db: Session = Depends(get_db),
    body: StaffFunctionCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create Staff Function

        - **name**: required
    """
    Authorize.jwt_required()
    return staff_function_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffFunctionRead,
            summary="Get Staff Function by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Staff Function by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return staff_function_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffFunctionRead,
            summary="Update Staff Function")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: StaffFunctionUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update Staff Function

        - **id**: UUID - required
        - **name**: required
    """
    Authorize.jwt_required()
    return staff_function_service.update(db, db_obj=staff_function_service.get_by_id(db, id), obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Staff Function")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete Staff Function

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    staff_function_service.remove(db, id)
