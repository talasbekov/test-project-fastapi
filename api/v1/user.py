import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import UserRead, UserUpdate, UserShortRead, TableUserRead
from services import user_service

router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())], response_model=List[UserRead], summary="Get all Users")
async def get_all(
    *,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    hr_document_template_id: uuid.UUID = None,
    filter: str = "",
    skip: int = 0,
    limit: int = 10
):
    """
    Get all Users

    - **hr_document_template_id**: str - The value which returns filtered results by hr_document_template_id. This parameter is optional and defaults to None
    - **filter**: str - The value which returns filtered results. This parameter is optional and defaults to None
    - **skip**: int - The number of users to skip before returning the results. This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of users to return in response. This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return user_service.get_all(db, hr_document_template_id, filter.lstrip().rstrip(), skip, limit)


@router.get("/archived", dependencies=[Depends(HTTPBearer())], response_model=TableUserRead, summary="Get all Users")
async def get_all_archived(
    *, db: Session = Depends(get_db), Authorize: AuthJWT = Depends(), filter: str = "", skip: int = 0, limit: int = 10
):
    """
     Get all Users
    - **filter**: str - The value which returns filtered results. This parameter is optional and defaults to None
    - **skip**: int - The number of users to skip before returning the results. This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of users to return in response. This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    users, total = user_service.get_all_archived(
        db, filter.lstrip().rstrip(), skip, limit, user_id)
    return TableUserRead(total=total, users=users)


@router.get("/active", dependencies=[Depends(HTTPBearer())], response_model=List[UserRead], summary="Get all Users")
async def get_all_active(
    *, db: Session = Depends(get_db), Authorize: AuthJWT = Depends(), filter: str = "", skip: int = 0, limit: int = 10
):
    """
     Get all Users
    - **filter**: str - The value which returns filtered results. This parameter is optional and defaults to None
    - **skip**: int - The number of users to skip before returning the results. This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of users to return in response. This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    users, total = user_service.get_all_active(
        db, filter.lstrip().rstrip(), skip, limit, user_id)
    return TableUserRead(total=total, users=users)


@router.get(
    "/jurisdiction",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[UserRead],
    summary="Get all Users by Jurisdiction",
)
async def get_all_by_jurisdiction(
    *, db: Session = Depends(get_db), Authorize: AuthJWT = Depends(), skip: int = 0, limit: int = 100
):
    """
     Get all Users by juridction

    - **skip**: int - The number of users to skip before returning the results. This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of users to return in the response. This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return user_service.get_by_jurisdiction(db, Authorize.get_jwt_subject(), skip, limit)


@router.get(
    "/staff-unit/{id}",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[UserRead],
    summary="Get all Users by Staff Unit",
)
async def get_all_by_staff_unit(*, db: Session = Depends(get_db), Authorize: AuthJWT = Depends(), id: uuid.UUID):
    """
     Get all Users by Staff Unit

    - **id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    return user_service.get_by_staff_unit(db, id)


@router.patch(
    "/{id}/", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(HTTPBearer())], response_model=UserRead
)
async def update_user_patch(
    *, db: Session = Depends(get_db), id: uuid.UUID, body: UserUpdate, Authorize: AuthJWT = Depends()
):
    """
    Update User

    - **id**: UUID - id of the User.
    - **email**: string required and should be a valid email format.
    - **first_name**: required.
    - **last_name**: required.
    - **father_name**: optional.
    - **icon**: image with url format. This parameter is optional.
    - **call_sign**: required.
    - **id_number**: unique employee number. This parameter is required.
    - **phone_number**: format (+77xxxxxxxxx). This parameter is optional.
    - **address**: optional.
    - **status**: the current status of the employee (e.g. "working", "on vacation", "sick", etc.). This parameter is optional.
    - **status_till**: the date when the current status of the employee will end. This parameter is optional.
    """
    Authorize.jwt_required()
    return user_service.update_user_patch(db, id, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())], response_model=UserRead, summary="Get User by id")
async def get_by_id(*, db: Session = Depends(get_db), id: uuid.UUID, Authorize: AuthJWT = Depends()):
    """
    Get User by id

    - **id**: UUID - required
    """
    Authorize.jwt_required()
    return user_service.get_by_id(db, id)


@router.get("/fields", dependencies=[Depends(HTTPBearer())], summary="Get fields")
async def get_fields(*, Authorize: AuthJWT = Depends()):
    """
    Get fields

    This endpoint does not accept any parameters and returns all fields.
    """
    Authorize.jwt_required()
    return user_service.get_fields()


@router.get("/profile")
async def get_profile(*, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    id = Authorize.get_jwt_subject()
    return user_service.get_by_id(db, id)


@router.get("/templates/{user_id}/")
async def get_templates(
    *,
    db: Session = Depends(get_db),
    user_id: uuid.UUID,
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return user_service.get_available_templates(db, user_id, skip, limit)


@router.get("/short/{id}/", response_model=UserShortRead)
async def get_short_user(*, db: Session = Depends(get_db), id: uuid.UUID, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return user_service.get_by_id(db, id)
