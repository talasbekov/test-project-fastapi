import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import StaffDivisionEnum
from schemas import (
    NewArchiveStaffUnitCreate,
    ArchiveStaffUnitRead,
    ArchiveStaffUnitFunctions,
    NewArchiveStaffUnitUpdate,
    ArchiveServiceStaffFunctionRead,
    ArchiveDocumentStaffFunctionRead,
    ArchiveStaffUnitUpdateDispose,
)
from services import (rank_service,
                      archive_staff_unit_service,
                      increment_changes_size,
                      archive_staff_division_service,
                      )

router = APIRouter(prefix="/archive_staff_unit", tags=["ArchiveStaffUnit"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ArchiveStaffUnitRead],
            summary="Get all Staff Units")
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    """
       Get all Staff Units

       - **skip**: int - The number of staff units to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff units to return in the response. This parameter is optional and defaults to 10.
   """
    Authorize.jwt_required()
    return archive_staff_unit_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ArchiveStaffUnitRead,
             summary="Create Staff Unit")
async def create(*,
    db: Session = Depends(get_db),
    body: NewArchiveStaffUnitCreate,
    Authorize: AuthJWT = Depends()
):
    """
        Create Staff Unit

        - **name**: required
        - **max_rank_id**: UUID - required and should exist in the database
        - **description**: a long description. This parameter is optional.
    """
    Authorize.jwt_required()
    return archive_staff_unit_service.create_staff_unit(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ArchiveStaffUnitRead,
            summary="Update Staff Unit")
async def update(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    body: NewArchiveStaffUnitUpdate,
    Authorize: AuthJWT = Depends()
):
    """
        Update Staff Unit

        - **id**: UUID - required
        - **name**: required
        - **max_rank_id**: UUID - required and should exist in the database
        - **description**: a long description. This parameter is optional.
    """
    Authorize.jwt_required()
    return archive_staff_unit_service.update_staff_unit(
        db,
        archive_staff_unit_service.get_by_id(db, id),
        body)


@router.put("/disposition/all/", dependencies=[Depends(HTTPBearer())],
            response_model=list[ArchiveStaffUnitRead],
            summary="Dispose all Staff Units by ids")
async def send_to_disposition(*,
    db: Session = Depends(get_db),
    body: ArchiveStaffUnitUpdateDispose,
    Authorize: AuthJWT = Depends()
):
    """
        Update Archive Staff Unit

        - **staff_unit_ids**: List of the UUIDs - required
        - **staff_list_id**: UUID - required
    """
    Authorize.jwt_required()
    archive_staff_division_id = archive_staff_division_service.get_by_name(
        db, StaffDivisionEnum.DISPOSITION.value, body.staff_list_id).id
    return archive_staff_unit_service.dispose_all_units(db, body.staff_unit_ids, archive_staff_division_id)




@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ArchiveStaffUnitRead,
            summary="Get Staff Unit by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Staff Unit by id

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    return archive_staff_unit_service.get_by_id(db, id)


@router.get("user/{user_id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ArchiveStaffUnitRead,
            summary="Get Staff Unit by id")
async def get_by_id(*,
    db: Session = Depends(get_db),
    user_id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get Staff Unit by user

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    return archive_staff_unit_service.get_by_user(db, user_id)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Staff Unit")
async def delete(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Delete Staff Unit

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    increment_changes_size(db, archive_staff_unit_service.get_by_id(db, id).staff_division.staff_list)
    archive_staff_unit_service.remove(db, id)


@router.get('/get-service-staff-functions/{id}', dependencies=[Depends(HTTPBearer())],
            response_model=List[ArchiveServiceStaffFunctionRead],
            summary="Get ServiceStaffFunctions by StaffUnit id")
async def get_service_staff_functions(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get ServiceStaffFunctions by StaffUnit id

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    return archive_staff_unit_service.get_service_staff_functions(db, id)


@router.post("/add-service-staff-function", dependencies=[Depends(HTTPBearer())],
             summary="Add ServiceStaffFunction")
async def add_service_staff_function(*,
    db: Session = Depends(get_db),
    body: ArchiveStaffUnitFunctions,
    Authorize: AuthJWT = Depends()
):
    """
        Add ServiceStaffFunction to StaffUnit

    """
    Authorize.jwt_required()
    archive_staff_unit_service.add_service_staff_function(db, body)


@router.post("/remove-service-staff-function", dependencies=[Depends(HTTPBearer())],
             summary="Remove ServiceStaffFunction")
async def remove_service_staff_function(*,
    db: Session = Depends(get_db),
    body: ArchiveStaffUnitFunctions,
    Authorize: AuthJWT = Depends()
):
    """
        Remove ServiceStaffFunction from StaffUnit

    """
    Authorize.jwt_required()
    archive_staff_unit_service.remove_service_staff_function(db, body)


@router.get('/get-document-staff-functions/{id}', dependencies=[Depends(HTTPBearer())],
            response_model=List[ArchiveDocumentStaffFunctionRead],
            summary="Get DocumentStaffFunctions by StaffUnit id")
async def get_document_staff_functions(*,
    db: Session = Depends(get_db),
    id: uuid.UUID,
    Authorize: AuthJWT = Depends()
):
    """
        Get DocumentStaffFunctions by StaffUnit id

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    return archive_staff_unit_service.get_document_staff_functions(db, id)


@router.post("/add-document-staff-function", dependencies=[Depends(HTTPBearer())],
             summary="Add DocumentStaffFunction")
async def add_document_staff_function(*,
    db: Session = Depends(get_db),
    body: ArchiveStaffUnitFunctions,
    Authorize: AuthJWT = Depends()
):
    """
        Add DocumentStaffFunction to StaffUnit

    """
    Authorize.jwt_required()
    archive_staff_unit_service.add_document_staff_function(db, body)


@router.post("/remove-document-staff-function", dependencies=[Depends(HTTPBearer())],
             summary="Remove DocumentStaffFunction")
async def remove_document_staff_function(*,
    db: Session = Depends(get_db),
    body: ArchiveStaffUnitFunctions,
    Authorize: AuthJWT = Depends()
):
    """
        Remove DocumentStaffFunction from StaffUnit

    """
    Authorize.jwt_required()
    archive_staff_unit_service.remove_document_staff_function(db, body)
