import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (StaffDivisionCreate, StaffDivisionRead,
                     StaffDivisionUpdate, StaffDivisionUpdateParentGroup,
                     StaffDivisionTypeRead)
from services import staff_division_service, staff_division_type_service

router = APIRouter(prefix="/staff_division", tags=["StaffDivision"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffDivisionRead],
            summary="Get all Staff Divisions")
async def get_all(*,
    db: Session = Depends(get_db),
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
    return staff_division_service.get_all_except_special(db, skip, limit)


@router.get("/departments/", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffDivisionRead],
            summary="Get all Staff Divisions")
async def get_departments(*,
    db: Session = Depends(get_db),
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
    return staff_division_service.get_all_departments(db, skip, limit)

@router.get("/division_parents/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffDivisionRead,
            summary="Get Staff Division and all his parents")
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
    return staff_division_service.get_division_parents_by_id(db, id)

@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=StaffDivisionRead,
             summary="Create Staff Division")
async def create(*,
    db: Session = Depends(get_db),
    body: StaffDivisionCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create Staff Division

        - **parent_group_id**: the id of the parent group. This parameter is optional.
        - **name**: required
        - **description**: a long description. This parameter is optional.
    """
    Authorize.jwt_required()
    return staff_division_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffDivisionRead,
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
    return staff_division_service.get_by_id(db, id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffDivisionRead,
            summary="Update Staff Division")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: StaffDivisionUpdate,
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
    return staff_division_service.update(db, db_obj=staff_division_service.get_by_id(db, id), obj_in=body)


@router.post("/{id}/", status_code=status.HTTP_202_ACCEPTED,
              dependencies=[Depends(HTTPBearer())],
              response_model=StaffDivisionRead,
              summary="Update parent of Staff Division")
async def update_parent(*,
     db: Session = Depends(get_db),
     id: uuid.UUID,
     body: StaffDivisionUpdateParentGroup,
     Authorize: AuthJWT = Depends()
):
    """
        Update parent of Staff Division

        - **id**: UUID - staff division id. It is required
        - **parent_group_id**: the id of the parent group. It is required
    """
    Authorize.jwt_required()
    return staff_division_service.change_parent_group(db, id, body)


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
    staff_division_service.delete(db, id)

@router.get('/name/{id}', dependencies=[Depends(HTTPBearer())],
            summary="Get Staff Division by id")
async def get_full_name_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Staff Division by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    full_name, full_nameKZ = staff_division_service.get_full_name(db, id)
    return {"name": full_name, "nameKZ": full_nameKZ}

@router.get("/types", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffDivisionTypeRead],
            summary="Get Staff Division types")
async def get_division_types(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
       Get all Staff Division Types
    """
    Authorize.jwt_required()
    return staff_division_type_service.get_multi(db,skip=skip, limit=limit)