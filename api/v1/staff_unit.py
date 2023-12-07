import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (
    StaffUnitCreate,
    StaffUnitRead,
    StaffUnitUpdate,
    StaffUnitFunctions,
    DocumentStaffFunctionRead,
    ServiceStaffFunctionRead,
    StaffUnitCreateWithPosition,
    StaffUnitFunctionsByPosition,
    StaffUnitMatreshkaOptionReadPagination
)
from services import staff_unit_service

router = APIRouter(
    prefix="/staff_unit",
    tags=["StaffUnit"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffUnitRead],
            summary="Get all Staff Units")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    """
       Get all Staff Units

       - **skip**: int - The number of staff units
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff units
            to return in the response.
            This parameter is optional and defaults to 10.
   """
    Authorize.jwt_required()
    return staff_unit_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=StaffUnitRead,
             summary="Create Staff Unit")
async def create(*,
                 db: Session = Depends(get_db),
                 body: StaffUnitCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Staff Unit

        - **name**: required
        - **max_rank_id**: UUID - required and should exist in the database
        - **description**: a long description. This parameter is optional.
    """
    Authorize.jwt_required()
    return staff_unit_service.create(db, body)


@router.post("/position/",
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=StaffUnitRead,
             summary="Create Staff Unit")
async def create_with_position(*,
                               db: Session = Depends(get_db),
                               body: StaffUnitCreateWithPosition,
                               Authorize: AuthJWT = Depends()
                               ):
    """
        Create Staff Unit with new position

        - **max_rank_id**: UUID - required and should exist in the database
    """
    Authorize.jwt_required()
    return staff_unit_service.create_with_position(db, body)


@router.put("/{id}/",
            dependencies=[Depends(HTTPBearer())],
            response_model=StaffUnitRead,
            summary="Update Staff Unit")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: StaffUnitUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Staff Unit

        - **id**: UUID - required
        - **name**: required
        - **position_id**: id of position.
            This parameter is optional.
        - **staff_division_id**: id of staff_division.
            This parameter is optional.
    """
    Authorize.jwt_required()
    return staff_unit_service.update(
        db=db,
        db_obj=staff_unit_service.get_by_id(db, str(id)),
        obj_in=body)


@router.get("/{id}/",
            dependencies=[Depends(HTTPBearer())],
            response_model=StaffUnitRead,
            summary="Get Staff Unit by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Staff Unit by id

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    return staff_unit_service.get_by_id(db, str(id))


@router.delete("/{id}/",
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Staff Unit")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Staff Unit

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    staff_unit_service.remove(db, str(id))


@router.get('/get-service-staff-functions/{id}',
            dependencies=[Depends(HTTPBearer())],
            response_model=List[ServiceStaffFunctionRead],
            summary="Get ServiceStaffFunctions by StaffUnit id")
async def get_service_staff_functions(*,
                                      db: Session = Depends(get_db),
                                      id: str,
                                      Authorize: AuthJWT = Depends()
                                      ):
    """
        Get ServiceStaffFunctions by StaffUnit id

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    return staff_unit_service.get_service_staff_functions(db, str(id))


@router.post("/add-service-staff-function", dependencies=[Depends(HTTPBearer())],
             summary="Add ServiceStaffFunction")
async def add_service_staff_function(*,
                                     db: Session = Depends(get_db),
                                     body: StaffUnitFunctions,
                                     Authorize: AuthJWT = Depends()
                                     ):
    """
        Add ServiceStaffFunction to StaffUnit

    """
    Authorize.jwt_required()
    staff_unit_service.add_service_staff_function(db, body)


@router.post("/remove-service-staff-function", dependencies=[Depends(HTTPBearer())],
             summary="Remove ServiceStaffFunction")
async def remove_service_staff_function(*,
                                        db: Session = Depends(get_db),
                                        body: StaffUnitFunctions,
                                        Authorize: AuthJWT = Depends()
                                        ):
    """
        Remove ServiceStaffFunction from StaffUnit

    """
    Authorize.jwt_required()
    staff_unit_service.remove_service_staff_function(db, body)


@router.get('/get-document-staff-functions/{id}', dependencies=[Depends(HTTPBearer())],
            response_model=List[DocumentStaffFunctionRead],
            summary="Get DocumentStaffFunctions by StaffUnit id")
async def get_document_staff_functions(*,
                                       db: Session = Depends(get_db),
                                       id: str,
                                       Authorize: AuthJWT = Depends()
                                       ):
    """
        Get DocumentStaffFunctions by StaffUnit id

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    return staff_unit_service.get_document_staff_functions(db, str(id))


@router.post("/add-document-staff-function", dependencies=[Depends(HTTPBearer())],
             summary="Add DocumentStaffFunction")
async def add_document_staff_function(*,
                                      db: Session = Depends(get_db),
                                      body: StaffUnitFunctions,
                                      Authorize: AuthJWT = Depends()
                                      ):
    """
        Add DocumentStaffFunction to StaffUnit

    """
    Authorize.jwt_required()
    staff_unit_service.add_document_staff_function(db, body)


@router.post("/add-document-staff-function/position",
             dependencies=[Depends(HTTPBearer())],
             summary="Add DocumentStaffFunction")
async def add_document_staff_function_by_position(*,
                                                  db: Session = Depends(
                                                      get_db),
                                                  body: StaffUnitFunctionsByPosition,
                                                  Authorize: AuthJWT = Depends()
                                                  ):
    """
        Add DocumentStaffFunction to StaffUnit

    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    staff_unit_service.add_document_staff_function_by_position(db, body, role)


@router.post("/remove-document-staff-function", dependencies=[Depends(HTTPBearer())],
             summary="Remove DocumentStaffFunction")
async def remove_document_staff_function(*,
                                         db: Session = Depends(get_db),
                                         body: StaffUnitFunctions,
                                         Authorize: AuthJWT = Depends()
                                         ):
    """
        Remove DocumentStaffFunction from StaffUnit

    """
    Authorize.jwt_required()
    staff_unit_service.remove_document_staff_function(db, body)

@router.get("/staff_division/{id}/",
            dependencies=[Depends(HTTPBearer())],
            response_model=StaffUnitMatreshkaOptionReadPagination,
            summary="Get Staff Units by staff_division_id")
async def get_by_staff_division_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    skip: int = 0,
                    limit: int = 10,
                    filter: str = '',
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Staff Units by staff_division_id

        - **staff_division_id** - UUID - required
        - **skip**: int - The number of staff units
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of staff units
            to return in the response.
            This parameter is optional and defaults to 10.
    """
    Authorize.jwt_required()
    return staff_unit_service.get_all_by_staff_division_id(db, str(id), skip, limit, filter)