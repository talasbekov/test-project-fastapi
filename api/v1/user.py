import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import User
from schemas import UserCreate, UserPermission, UserServiceFunction, UserRead, UserUpdate, UserGroupUpdate
from services import user_service

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())], response_model=List[UserRead],
            summary="Get all Users")
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    """
        Get all Users

       - **skip**: int - The number of users to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of users to return in the response. This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return user_service.get_multi(db, skip, limit)


@router.patch("/{id}/", status_code=status.HTTP_202_ACCEPTED,
              dependencies=[Depends(HTTPBearer())],
              response_model=UserRead)
async def update_user_patch(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: UserUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update User

        - **id**: UUID - id of the User.
        - **email**: string required and should be a valid email format.
        - **first_name**: required.
        - **last_name**: required.
        - **father_name**: optional.
        - **group_id**: UUID - required and should exist in the database
        - **position_id**: UUID - required and should exist in the database.
        - **icon**: image with url format. This parameter is optional.
        - **call_sign**: required.
        - **id_number**: unique employee number. This parameter is required.
        - **phone_number**: format (+77xxxxxxxxx). This parameter is optional.
        - **address**: optional.
        - **birthday**: format (YYYY-MM-DD). This parameter is optional.
        - **status**: the current status of the employee (e.g. "working", "on vacation", "sick", etc.). This parameter is optional.
        - **status_till**: the date when the current status of the employee will end. This parameter is optional.
    """
    Authorize.jwt_required()
    return user_service.update_user_patch(db, id, body)


@router.get('/{id}/', dependencies=[Depends(HTTPBearer())],
            response_model=UserRead,
            summary="Get User by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get User by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return user_service.get_by_id(db, id)


@router.get('/fields', dependencies=[Depends(HTTPBearer())],
            summary="Get fields")
async def get_fields(*,
    Authorize: AuthJWT = Depends()
):
    """
        Get fields

        This endpoint does not accept any parameters and returns all fields.
    """
    Authorize.jwt_required()
    return user_service.get_fields()


@router.post("/add-permission", dependencies=[Depends(HTTPBearer())],
             summary="Add Permission")
async def add_permission(*,
    db: Session = Depends(get_db),
    body: UserPermission,
    Authorize: AuthJWT = Depends()
):
    """
        Add Permission to user

        - **user_id**: UUID - the ID of the user to add the permission. It is required and should exist in database.
        - **permission_ids**: UUID - A list of IDs of the permissions to add. This parameter is required and should exist in database.
    """
    Authorize.jwt_required()
    user_service.add_permission(db, body)


@router.post("/remove-permission", dependencies=[Depends(HTTPBearer())],
             summary="Remove Permission")
async def remove_permission(*,
    db: Session = Depends(get_db),
    body: UserPermission,
    Authorize: AuthJWT = Depends()
):
    """
        Remove Permission from user

        - **user_id**: UUID - the ID of the user to remove the permission. It is required and should exist in database.
        - **permission_ids**: UUID - A list of IDs of the permissions to remove. This parameter is required and should exist in database.
    """
    Authorize.jwt_required()
    user_service.remove_permission(db, body)


@router.get("/profile")
async def get_profile(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    id = Authorize.get_jwt_subject()
    return user_service.get_by_id(db, id)


@router.post("/add-service-function", dependencies=[Depends(HTTPBearer())],
             summary="Add ServiceFunction")
async def add_service_function(*,
    db: Session = Depends(get_db),
    body: UserServiceFunction,
    Authorize: AuthJWT = Depends()
):
    """
        Add ServiceFunction to user

        - **user_id**: UUID - the ID of the user to add the permission. It is required and should exist in database.
        - **service_function_ids**: UUID - A list of IDs of the permissions to add. This parameter is required and should exist in database.
    """
    Authorize.jwt_required()
    user_service.add_service_function(db, body)


@router.post("/remove-service-function", dependencies=[Depends(HTTPBearer())],
             summary="Remove ServiceFunction")
async def remove_service_function(*,
    db: Session = Depends(get_db),
    body: UserServiceFunction,
    Authorize: AuthJWT = Depends()
):
    """
        Remove ServiceFunction from user

        - **user_id**: UUID - the ID of the user to remove the permission. It is required and should exist in database.
        - **service_function_ids**: UUID - A list of IDs of the permissions to remove. This parameter is required and should exist in database.
    """
    Authorize.jwt_required()
    user_service.remove_service_function(db, body)
