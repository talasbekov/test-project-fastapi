import uuid

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import (BspPlanRead,
                     BspPlanUpdate,
                     BspPlanCreate,
                     BspPlanReadPagination,)

from services import plan_service


router = APIRouter(prefix="/plan",
                   tags=["BspPlan"],
                   dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=BspPlanReadPagination,
            summary="Get all BspPlan")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all BspPlans

    - **skip**: int - The number of BspPlan
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of BspPlan
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return plan_service.get_multi(db, skip, limit)

@router.get("/draft/", dependencies=[Depends(HTTPBearer())],
            response_model=BspPlanReadPagination,
            summary="Get all BspPlan")
async def get_all_draft(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all draft BspPlans

    - **skip**: int - The number of BspPlan
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of BspPlan
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return plan_service.get_all_draft(db, skip, limit)

@router.get("/signed/", dependencies=[Depends(HTTPBearer())],
            response_model=BspPlanReadPagination,
            summary="Get all BspPlan")
async def get_all_signed(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all draft BspPlans

    - **skip**: int - The number of BspPlan
        to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of BspPlan
        to return in the response.
        This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return plan_service.get_all_signed(db, skip, limit)

@router.post("/sign/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BspPlanRead,
            summary="Get all BspPlan")
async def sign(*,
                  db: Session = Depends(get_db),
                  id: str,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Sign BspPlan
   """
    Authorize.jwt_required()
    return plan_service.sign(db, str(id))

@router.post("/draft/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BspPlanRead,
            summary="Send BspPlan to draft")
async def send_to_draft(*,
                  db: Session = Depends(get_db),
                  id: str,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Send BspPlan to draft
   """
    Authorize.jwt_required()
    return plan_service.send_to_draft_full(db, str(id))

@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BspPlanRead,
            summary="Get BspPlan by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get BspPlan by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return plan_service.get_by_id(db, str(id))

@router.get("/duplicate/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BspPlanRead,
            summary="Duplicate BspPlan by id")
async def duplicate(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Duplicate BspPlan by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return plan_service.duplicate(db, str(id))

@router.post("/", dependencies=[Depends(HTTPBearer())],
            response_model=BspPlanRead,
            summary="Create BspPlan")
async def create(*,
                 db: Session = Depends(get_db),
                 body: BspPlanCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create BspPlan

    """
    Authorize.jwt_required()
    return plan_service.create(db, body)

@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BspPlanRead,
            summary="Update BspPlan")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: BspPlanUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update BspPlan

    """
    Authorize.jwt_required()
    return plan_service.update(
        db,
        db_obj=plan_service.get_by_id(db, str(id)),
        obj_in=body)

@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=BspPlanRead,
            summary="Delete BspPlan")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete BspPlan

    """
    Authorize.jwt_required()
    return plan_service.remove(db, str(id))
