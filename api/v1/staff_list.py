import uuid
import datetime
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from celery.result import AsyncResult

from core import get_db
from schemas import (
    StaffListRead,
    StaffListUpdate,
    StaffListUserCreate,
    StaffListStatusRead,
    StaffListApplyRead
)
from services import staff_list_service
from tasks import task_create_draft, task_apply_staff_list

router = APIRouter(
    prefix="/staff_list",
    tags=["StaffList"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffListRead],
            summary="Get all Staff Lists")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Staff Lists

       - **skip**: int - The number of staff divisions
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff divisions
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return staff_list_service.get_multi(db, skip, limit)


@router.get("/drafts/", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffListStatusRead],
            summary="Get Staff List history")
async def get_drafts(*,
                     db: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(),
                     skip: int = 0,
                     limit: int = 100,
                     filter: str = '',
                     ):
    """
       Get Staff Lists drafts

       - **skip**: int - The number of staff divisions
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff divisions
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return staff_list_service.get_drafts(db, skip, limit, filter)


@router.get("/signed/", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffListStatusRead],
            summary="Get Staff List history")
async def get_signed(*,
                     db: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(),
                     skip: int = 0,
                     limit: int = 100,
                     filter: str = ''
                     ):
    """
       Get Staff Lists signed

       - **skip**: int - The number of staff divisions
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff divisions
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return staff_list_service.get_signed(db, skip, limit, filter)


@router.get("/task-status/{task_id}",
            status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(HTTPBearer())],
            summary="Staff List task status")
async def get_result(task_id: str):
    result = AsyncResult(task_id)
    if result.ready():
        return StaffListRead(**result.result)
    else:
        return {"status": AsyncResult(task_id).state}


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=dict,
             summary="Create Staff List")
async def create(*,
                 body: StaffListUserCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Staff List
        - **parent_group_id**: the id of the parent group. This parameter is optional.
        - **name**: required
        - **description**: a long description. This parameter is optional.
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    body = body.dict()
    result = task_create_draft.delay(user_id=str(Authorize.get_jwt_subject()),
                                     obj_in=body,
                                     current_user_role_id=role)

    return {"task_id": result.id}


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=StaffListRead,
            summary="Get Staff List by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Staff List by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return staff_list_service.get_by_id(db, id)


@router.post("/apply/{id}/", dependencies=[Depends(HTTPBearer())],
             response_model=StaffListApplyRead,
             summary="Apply Staff List")
async def apply_staff_list(*,
                           id: uuid.UUID,
                           signed_by: str,
                           document_creation_date: datetime.date,
                           rank: str,
                           document_number: str,
                           document_link: str = None,
                           Authorize: AuthJWT = Depends()
                           ):
    """
        Update Staff List

        - **id**: UUID - id of the Staff List.
        - **signed_by**: required
        - **document_creation_date**: required
        - **date_from**: date - format (YYYY-MM-DD).
            This parameter is required.
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    current_user_id = Authorize.get_jwt_subject()
    result = task_apply_staff_list.delay(id,
                                         signed_by,
                                         document_creation_date,
                                         current_user_id,
                                         role,
                                         rank,
                                         document_number,
                                         document_link)

    return {"task_id": result.id}


@router.put("/{id}/",
            dependencies=[Depends(HTTPBearer())],
            response_model=StaffListRead,
            summary="Update Staff List")
async def update(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 body: StaffListUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Staff List

        - **id**: UUID - id of the Staff Division.
        - **parent_group_id**: the id of the parent group.
            This parameter is optional.
        - **name**: required
        - **description**: a long description.
            This parameter is optional.
    """
    Authorize.jwt_required()
    return staff_list_service.update(db, id, body)


@router.delete("/{id}/",
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Staff List")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: uuid.UUID,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Staff List

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    staff_list_service.remove(db, id)

@router.post("/duplicate/{id}/",
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=StaffListRead,
             summary="Duplicate Staff List")
async def duplicate(*,
                    db: Session = Depends(get_db),
                    id: uuid.UUID,
                    body: StaffListUserCreate,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Duplicate Staff List

        - **id**: UUID - id of the Staff List.
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return staff_list_service.duplicate(
        db,
        staff_list_id=id,
        user_id=Authorize.get_jwt_subject(),
        obj_in=body,
        current_user_role_id=role)