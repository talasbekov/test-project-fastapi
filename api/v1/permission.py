import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from core import get_db
from schemas import PermissionCreate, PermissionUpdate, PermissionRead
from services import permission_service

router = APIRouter(prefix="/permissions", tags=["Permissions"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[PermissionRead],
            summary="Get all Permissions")
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    """
        Get all Permissions

        - **skip**: int - The number of permissions to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of permissions to return in the response. This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return permission_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=PermissionRead,
             summary="Create Permission")
async def create(*,
    db: Session = Depends(get_db),
    body: PermissionCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create Permission

        - **name**: required
    """
    Authorize.jwt_required()
    return permission_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PermissionRead,
            summary="Update Permission")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: PermissionUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update Permission

        - **id**: UUID - required
        - **name**: required
    """
    Authorize.jwt_required()
    return permission_service.update(
        db=db,
        db_obj=permission_service.get_by_id(db, id),
        obj_in=body)

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PermissionRead,
            summary="Get Permission by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Permission by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return permission_service.get_by_id(db, id)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Permission")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete Permission

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    permission_service.remove(db, id)
