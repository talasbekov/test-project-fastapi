import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (
    PermissionCreate,
    PermissionRead,
    PermissionUpdate,
    PermissionTypeRead,
    PermissionPaginationRead,
)
from services import permission_service

router = APIRouter(
    prefix="/permissions", tags=["Permissions"], dependencies=[Depends(HTTPBearer())]
)


@router.get(
    "",
    dependencies=[Depends(HTTPBearer())],
    response_model=PermissionPaginationRead,
    summary="Get all Permissions",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Permissions

    - **skip**: int - The number of permissions
         to skip before returning the results.
         This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of permissions
         to return in the response.
         This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return permission_service.get_multi(db, skip, limit)


@router.get(
    "/has_permission",
    dependencies=[Depends(HTTPBearer())],
    response_model=bool,
    summary="If user has permission",
)
async def has_permission(
    *, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    """
    Check if authorized user has permission for permission_type

    - **permission_type**: str - permission_type name
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    role = Authorize.get_raw_jwt()["role"]
    permissions = Authorize.get_raw_jwt()["permissions"]
    return permission_service.has_permission(
        db, str(user_id), str(role), list(permissions)
    )


@router.get(
    "/user_permissions",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[PermissionRead],
    summary="Get all Permissions of user",
)
async def has_permission(
    *,
    db: Session = Depends(get_db),
    user_id: str = None,
    Authorize: AuthJWT = Depends()
):
    """
    Get all permissions of user

    - **permission_type**: str - permission_type name
    """
    Authorize.jwt_required()
    if user_id is None:
        user_id = Authorize.get_jwt_subject()
    return permission_service.get_permissions_by_user(db, str(user_id))


@router.get(
    "/types",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[PermissionTypeRead],
    summary="Get all Permissions Types",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Permissions Types

    - **skip**: int - The number of permission types
         to skip before returning the results.
         This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of permission types
         to return in the response.
         This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return permission_service.get_permission_types(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(HTTPBearer())],
    response_model=PermissionRead,
    summary="Create Permission",
)
async def create(
    *,
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


@router.get(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=PermissionRead,
    summary="Get Permission by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Get Permission by id

    - **id**: UUID - required
    """
    Authorize.jwt_required()
    return permission_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=PermissionRead,
    summary="Update Permission",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: PermissionUpdate,
    Authorize: AuthJWT = Depends()
):
    """
    Update Permission

    - **id**: UUID - the ID of permission to update. This is required.
    - **name**: required.
    """
    Authorize.jwt_required()
    return permission_service.update(
        db, db_obj=permission_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(HTTPBearer())],
    summary="Delete Permission",
)
async def delete(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Delete Permission

    - **id**: UUID - required
    """
    Authorize.jwt_required()
    permission_service.remove(db, str(id))
