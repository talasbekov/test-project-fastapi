import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (ArchiveStaffDivisionRead, ArchiveStaffDivisionUpdateParentGroup, NewArchiveStaffDivisionCreate,
                     NewArchiveStaffDivisionUpdate)
from services import archive_staff_division_service, staff_list_service

router = APIRouter(prefix="/archive_staff_division", tags=["ArchiveStaffDivision"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ArchiveStaffDivisionRead],
            summary="Get all Staff Divisions")
async def get_all(*,
    db: Session = Depends(get_db),
    staff_list_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
       Get all Staff Divisions

       - **skip**: int - The number of staff divisions to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff divisions to return in the response. This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    staff_list_service.get_by_id(db, staff_list_id)
    return archive_staff_division_service.get_departments(db, staff_list_id, skip, limit)


@router.get("/division_parents/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ArchiveStaffDivisionRead,
            summary="Get Archive Staff Division and all his parents")
async def get_division_parents_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
       Get all Staff Divisions

       - **id**: uuid - The id of staff division. This parameter is required.
   """
    Authorize.jwt_required()
    return archive_staff_division_service.get_division_parents_by_id(db, id)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ArchiveStaffDivisionRead,
             summary="Create Staff Division")
async def create(*,
    db: Session = Depends(get_db),
    body: NewArchiveStaffDivisionCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create Staff Division

        - **parent_group_id**: the id of the parent group. This parameter is optional.
        - **name**: required
        - **description**: a long description. This parameter is optional.
    """
    Authorize.jwt_required()
    return archive_staff_division_service.create_staff_division(db, body)


@router.get("/duplicate/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ArchiveStaffDivisionRead,
            summary="Duplicate Staff Division by id")
async def duplicate(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Staff Division by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return archive_staff_division_service.duplicate(db, id)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ArchiveStaffDivisionRead,
            summary="Get Staff Division by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Staff Division by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return archive_staff_division_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ArchiveStaffDivisionRead,
            summary="Update Staff Division")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: NewArchiveStaffDivisionUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update Staff Division

        - **id**: UUID - id of the Staff Division.
        - **parent_group_id**: the id of the parent group. This parameter is optional.
        - **name**: required
        - **description**: a long description. This parameter is optional.
    """
    Authorize.jwt_required()
    obj = archive_staff_division_service.get_by_id(db, id)
    return archive_staff_division_service.update_staff_division(db, obj, body)


@router.post("/{id}/", status_code=status.HTTP_202_ACCEPTED,
              dependencies=[Depends(HTTPBearer())],
              response_model=ArchiveStaffDivisionRead,
              summary="Update parent of Staff Division")
async def update_parent(*,
     db: Session = Depends(get_db),
     id: uuid.UUID,
     body: ArchiveStaffDivisionUpdateParentGroup,
     Authorize: AuthJWT = Depends()
):
    """
        Update parent of Staff Division

        - **id**: UUID - staff division id. It is required
        - **parent_group_id**: the id of the parent group. It is required
    """
    Authorize.jwt_required()
    return archive_staff_division_service.change_parent_group(db, id, body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Staff Division")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authrorize: AuthJWT = Depends()
):
    """
        Delete Staff Division

        - **id**: UUID - required
    """
    Authrorize.jwt_required()
    archive_staff_division_service.remove(db, id)
