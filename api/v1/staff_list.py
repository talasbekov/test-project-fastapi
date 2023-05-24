import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import StaffListCreate, StaffListRead, StaffListUpdate, StaffListUserCreate, StaffListStatusRead
from services import staff_list_service, hr_document_service

router = APIRouter(prefix="/staff_list", tags=["StaffList"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffListRead],
            summary="Get all Staff Divisions")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Staff Lists

       - **skip**: int - The number of staff divisions to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff divisions to return in the response. This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return staff_list_service.get_multi(db, skip, limit)

@router.get("/drafts/", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffListStatusRead],
            summary="Get Staff List history")
async def get_history(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 100
):
    """
       Get Staff Lists drafts

       - **skip**: int - The number of staff divisions to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff divisions to return in the response. This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return staff_list_service.get_drafts(db, skip, limit)

@router.get("/signed/", dependencies=[Depends(HTTPBearer())],
            response_model=List[StaffListStatusRead],
            summary="Get Staff List history")
async def get_history(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 100
):
    """
       Get Staff Lists signed

       - **skip**: int - The number of staff divisions to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of staff divisions to return in the response. This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return staff_list_service.get_signed(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=StaffListRead,
             summary="Create Staff List")
async def create(*,
                 db: Session = Depends(get_db),
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

    return staff_list_service.create_by_user_id(db, user_id=Authorize.get_jwt_subject(), obj_in=body)


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


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
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
        - **parent_group_id**: the id of the parent group. This parameter is optional.
        - **name**: required
        - **description**: a long description. This parameter is optional.
    """
    Authorize.jwt_required()
    return staff_list_service.update(db, id, body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
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
    return staff_list_service.remove(db, id)


@router.post("/duplicate/{id}/", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
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
    return staff_list_service.duplicate(db, staff_list_id=id, user_id=Authorize.get_jwt_subject(), obj_in=body)
