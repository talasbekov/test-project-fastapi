import uuid

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from typing import List

from core import get_db
from schemas import CandidateStageInfoCreate, CandidateStageInfoRead, CandidateStageInfoUpdate
from services import candidate_stage_info_service

router = APIRouter(prefix="/candidate_stage_info", tags=["CandidateStageInfo"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[CandidateStageInfoRead],
            summary="Get all CandidateStageInfo")
async def get_all(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        Authorize: AuthJWT = Depends(),
        filter: str = None
):
    """
        Get all CandidateStageInfo.

        - **skip**: int - The number of CandidateStageInfo to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of CandidateStageInfo to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    role = Authorize.get_raw_jwt()['role']
    return candidate_stage_info_service.get_all_by_staff_unit_id(db, skip, limit, role)


@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateStageInfoRead,
            summary="Get a CandidateStageInfo by id")
async def get_by_id(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None
):
    """
        Get a CandidateStageInfo by id.

        - **id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    return candidate_stage_info_service.get_by_id(db, id)


@router.get("/all/candidate/{candidate_id}", dependencies=[Depends(HTTPBearer())],
            response_model=List[CandidateStageInfoRead],
            summary="Get all CandidateStageInfo by candidate_id")
async def get_all_by_candidate_id(
        db: Session = Depends(get_db),
        candidate_id: uuid.UUID = None,
        skip: int = 0,
        limit: int = 100,
        Authorize: AuthJWT = Depends(),
):
    """
        Get all CandidateStageInfo by candidate_id.

        - **candidate_id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    return candidate_stage_info_service.get_all_by_candidate_id(db, skip, limit, candidate_id)


@router.post("", dependencies=[Depends(HTTPBearer())],
             status_code=status.HTTP_201_CREATED,
             summary="Create a CandidateStageInfo",
             response_model=CandidateStageInfoRead)
async def create(
        db: Session = Depends(get_db),
        body: CandidateStageInfoCreate = None,
        Authorize: AuthJWT = Depends()
):
    """
        Create a CandidateStageInfo.

        - **candidate_id**: UUID - required and should exist in the database.
        - **candidate_stage_type_id**: UUID - required and should exist in the database.
        - **staff_unit_coordinate_id**: UUID - required and should exist in the database.
        - **is_waits**: bool - optional.
    """
    Authorize.jwt_required()
    return candidate_stage_info_service.create(db, body)


@router.patch("/{id}/sign", dependencies=[Depends(HTTPBearer())],
              summary="Sign a CandidateStageInfo",
              status_code=status.HTTP_202_ACCEPTED,
              response_model=CandidateStageInfoRead)
async def sign_candidate(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None,
):
    """
        Sign a CandidateStageInfo

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return candidate_stage_info_service.sign_candidate(db, id)


@router.patch("/{id}/reject", dependencies=[Depends(HTTPBearer())],
              summary="Sign a CandidateStageInfo",
              status_code=status.HTTP_202_ACCEPTED,
              response_model=CandidateStageInfoRead)
async def reject_candidate(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None,
):
    """
        Reject a CandidateStageInfo

        - **id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    return candidate_stage_info_service.reject_candidate(db, id)


@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateStageInfoRead,
            summary="Update a CandidateStageInfo")
async def update(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None,
        body: CandidateStageInfoUpdate = None
):
    """
        Update a CandidateStageInfo.

        - **id**: UUID - required and should exist in the database.
        - **candidate_id**: UUID - optional and should exist in the database.
        - **candidate_stage_type_id**: UUID - optional and should exist in the database.
        - **staff_unit_coordinate_id**: UUID - optional and should exist in the database.
        - **is_waits**: bool - optional.
        - **status**: str - optional.
    """
    Authorize.jwt_required()
    return candidate_stage_info_service.update(db,
                                               db_obj=candidate_stage_info_service.get_by_id(db, id),
                                               obj_in=body)


@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a CandidateStageInfo")
async def delete(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None
):
    """
        Delete a CandidateStageInfo.

        - **id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    candidate_stage_info_service.remove(db, id)
