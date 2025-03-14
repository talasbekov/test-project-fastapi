import uuid
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (UserRead,
                     UserUpdate,
                     UserShortRead,
                     TableUserRead,
                     UserShortReadStatusPagination,
                     UserShortReadFullNames,
                     TableUserReadActive,
                     DocumentReadForUser)
from models import PermissionTypeEnum
from services import user_service

router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(HTTPBearer())])


@router.get("",
            dependencies=[Depends(HTTPBearer())],
            response_model=TableUserRead,
            summary="Get all Users")
async def get_all(
    *,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    hr_document_template_id: str = None,
    filter: str = "",
    skip: int = 0,
    limit: int = 10
):
    """
    Get all Users

    - **hr_document_template_id**: str - The value which returns filtered
        results by hr_document_template_id.
        This parameter is optional and defaults to None
    - **filter**: str - The value which returns filtered results.
        This parameter is optional and defaults to None
    - **skip**: int - The number of users to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of users to return in response.
        This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    total, users = user_service.get_all(db,
                                hr_document_template_id,
                                filter.lstrip().rstrip(),
                                skip,
                                limit)
    return TableUserRead(total=total, users=users)


@router.get("/unemployed/{is_free}",
            dependencies=[Depends(HTTPBearer())],
            response_model=List[UserShortRead],
            summary="Get all Unemployed Users")
async def get_all_unemployed(
    is_free: bool = False,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """
    Get all Unemployed Users
    """
    Authorize.jwt_required()
    return user_service.get_all_unemployed(db, is_free, skip, limit)

@router.get("/get_all_short_read",
            dependencies=[Depends(HTTPBearer())],
            response_model=UserShortReadFullNames,
            summary="Get all Users Short Read Full Names")
async def get_all_full_name(
    *,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    hr_document_template_id: str = None,
    filter: str = "",
    skip: int = 0,
    limit: int = 10
):
    """
    Get all Users Full Name Short Read

    - **hr_document_template_id**: str - The value which returns filtered
        results by hr_document_template_id.
        This parameter is optional and defaults to None
    - **filter**: str - The value which returns filtered results.
        This parameter is optional and defaults to None
    - **skip**: int - The number of users to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of users to return in response.
        This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    total, users = user_service.get_all(db,
                                hr_document_template_id,
                                filter.lstrip().rstrip(),
                                skip,
                                limit)
    return UserShortReadFullNames(total=total, users=users)

@router.get("/get_all_heads_except_pgs", 
            dependencies=[Depends(HTTPBearer())],
            response_model=UserShortReadFullNames,
            summary="Get all Heads except PGS")
async def get_all_heads_except_pgs(*,
                                db: Session = Depends(get_db),
                                Authorize: AuthJWT = Depends()
                                ):
    Authorize.jwt_required()
    total, users = user_service.get_all_heads_except_pgs(db)
    return UserShortReadFullNames(total=total, users=users)


@router.get("/{user_id}/templates/",
            dependencies=[Depends(HTTPBearer())],
            summary="Check if user has access to template")
async def is_template_accessible_for_user(
    *,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    user_id: str,
    hr_document_template_id: str
):
    """
    Check if user has access to template

    - **user_id**: str - The value which returns filtered results by user_id.
    """
    Authorize.jwt_required()
    return user_service.is_template_accessible_for_user(
                db, user_id, hr_document_template_id)


@router.get("/archived",
            dependencies=[Depends(HTTPBearer())],
            response_model=TableUserRead,
            summary="Get all Users")
async def get_all_archived(
    *,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    filter: str = "",
    skip: int = 0,
    limit: int = 10
):
    """
     Get all Users
    - **filter**: str - The value which returns filtered results.
        This parameter is optional and defaults to None
    - **skip**: int - The number of users to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of users to return in response.
        This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    users, total = user_service.get_all_archived(
        db, filter.lstrip().rstrip(), skip, limit, user_id)
    return TableUserRead(total=total, users=users)


@router.get("/active",
            dependencies=[Depends(HTTPBearer())],
            response_model=TableUserReadActive,
            summary="Get all Users")
async def get_all_active(
    *,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    filter: str = "",
    skip: int = 0,
    limit: int = 10
):
    """
    Получает всех активных пользователей.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    users, total = user_service.get_all_active(db, filter.strip(), skip, limit, user_id)
    return TableUserReadActive(total=total, users=users)


@router.get("/active_old",
            dependencies=[Depends(HTTPBearer())],
            response_model=TableUserRead,
            summary="Get all Users")
async def get_all_active(
    *,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    filter: str = "",
    skip: int = 0,
    limit: int = 10
):
    """
     Get all Users
    - **filter**: str - The value which returns filtered results.
    This parameter is optional and defaults to None
    - **skip**: int - The number of users to skip before returning the results.
    This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of users to return in response.
    This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    users, total = user_service.get_all_active(
        db, filter.lstrip().rstrip(), skip, limit, user_id)
    return TableUserRead(total=total, users=users)


@router.get("/restricted/active",
            dependencies=[Depends(HTTPBearer())],
            response_model=TableUserRead,
            summary="Get all Users")
async def get_all_active_with_permission(
    *,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    filter: str = "",
    skip: int = 0,
    limit: int = 10
):
    """
     Get all Users
    - **filter**: str - The value which returns filtered results.
    This parameter is optional and defaults to None
    - **skip**: int - The number of users to skip before returning the results.
    This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of users to return in response.
    This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    decoded_token = Authorize.get_raw_jwt()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    permissions = decoded_token.get("permissions")
    if int(PermissionTypeEnum.VIEW_ALL_EMPLOYEES.value) not in permissions and \
            int(PermissionTypeEnum.VIEW_ALL_EMPLOYEES_BY_DEPARTMENT.value) not in permissions:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "You are not allowed")
    if int(PermissionTypeEnum.VIEW_ALL_EMPLOYEES_BY_DEPARTMENT.value) in permissions and \
            int(PermissionTypeEnum.VIEW_ALL_EMPLOYEES.value) not in permissions:
        users = user_service.get_users_by_staff_division(db, user.staff_unit.staff_division_id)
        return TableUserRead(total=len(users), users=users)
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
    *,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 100
):
    """
     Get all Users by juridction

    - **skip**: int - The number of users to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of users to return in the response.
        This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return user_service.get_by_jurisdiction(db,
                                            Authorize.get_jwt_subject(),
                                            skip,
                                            limit)


@router.get(
    "/staff-unit/{id}",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[UserRead],
    summary="Get all Users by Staff Unit",
)
async def get_all_by_staff_unit(*,
                                db: Session = Depends(get_db),
                                Authorize: AuthJWT = Depends(),
                                id: str):
    """
     Get all Users by Staff Unit

    - **id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    return user_service.get_all_by_staff_unit(db, str(id))


@router.get(
    "/position/{id}",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[UserRead],
    summary="Get all Users by Staff Unit",
)
async def get_all_by_position(*,
                                db: Session = Depends(get_db),
                                Authorize: AuthJWT = Depends(),
                                id: str):
    """
     Get all Users by Position

    - **id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    return user_service.get_all_by_position(db, str(id))


@router.get(
    "/schedule/{id}",
    dependencies=[Depends(HTTPBearer())],
    response_model=UserShortReadStatusPagination,
    summary="Get all Users by ScheduleYear",
)
async def get_all_by_schedule_id(*,
                             db: Session = Depends(get_db),
                             Authorize: AuthJWT = Depends(),
                             id: str,
                             skip: int,
                             limit: int
                                 ):
    """
     Get all Users by Plan

    - **id**: UUID - required and should exist in the database.
    - **skip**: int - The number of users to skip before returning the results.
    This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of users to return in response.
    This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return user_service.get_by_schedule_id(db, id, skip, limit)


@router.patch(
    "/{id}/",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(HTTPBearer())],
    response_model=UserRead
)
async def update_user_patch(
    *,
    db: Session = Depends(get_db),
    id: str,
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
    - **icon**: image with url format. This parameter is optional.
    - **x_sign**: required.
    - **id_number**: unique employee number. This parameter is required.
    - **phone_number**: format (+77xxxxxxxxx). This parameter is optional.
    - **address**: optional.
    - **status**: the current status of the employee
        (e.g. "working", "on vacation", "sick", etc.).
        This parameter is optional.
    - **status_till**: the date when the current status
        of the employee will end. This parameter is optional.
    """
    Authorize.jwt_required()
    return user_service.update_user_patch(db, str(id), body)


@router.get("/{id}/",
            dependencies=[Depends(HTTPBearer())],
            response_model=UserRead,
            summary="Get User by id")
async def get_by_id(
    *,
    db: Session = Depends(get_db),
    id: str,
    Authorize: AuthJWT = Depends()
):
    """
    Get User by id

    - **id**: UUID - required
    """
    Authorize.jwt_required()
    return user_service.get_by_id(db, str(id))


@router.get("/fields",
            dependencies=[Depends(HTTPBearer())], summary="Get fields")
async def get_fields(*, Authorize: AuthJWT = Depends()):
    """
    Get fields

    This endpoint does not accept any parameters and returns all fields.
    """
    Authorize.jwt_required()
    return user_service.get_fields()


@router.get("/profile")
async def get_profile(
    *,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    id = Authorize.get_jwt_subject()
    return user_service.get_by_id(db, str(id))


@router.get("/templates/{user_id}/",
            response_model=List[DocumentReadForUser]
            )
async def get_templates(
    *,
    db: Session = Depends(get_db),
    user_id: str,
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    return user_service.get_available_templates(db, str(user_id), skip, limit)


@router.get("/short/{id}/", response_model=UserShortRead)
async def get_short_user(
    *,
    db: Session = Depends(get_db),
    id: str,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.get_by_id(db, str(id))

@router.put("/add-rank/", response_model=UserShortRead)
def add_rank(
    *,
    db: Session = Depends(get_db),
    id: str,
    rank_id: str,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.update_user_rank(db, id, rank_id)

@router.post("/iins/", response_model=dict)
def get_short_user(
    *,
    db: Session = Depends(get_db),
    user_ids: List[str],
    candidate_ids: List[str],
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.get_all_iin_by_ids(db, user_ids, candidate_ids)

@router.get("/get_by_iin/{iin}/", response_model=UserShortRead)
async def get_user_by_iin(
    *,
    db: Session = Depends(get_db),
    iin: str,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return user_service.get_user_by_iin(db, iin)

@router.get("/get_eligible_for_vacancy/{staff_unit_id}/")
def get_eligible_for_vacancy(
    *,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    staff_unit_id: str,
    filter: str = "",
    skip: int = 0,
    limit: int = 10
):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return user_service.get_users_for_vacancy_fill(db, staff_unit_id, filter.lstrip().rstrip(), skip, limit, user_id)
    
