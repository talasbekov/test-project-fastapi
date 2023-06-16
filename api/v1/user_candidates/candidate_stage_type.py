import uuid

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from typing import List

from core import get_db
from schemas import CandidateStageTypeCreate, CandidateStageTypeRead, CandidateStageTypeUpdate
from services import candidate_stage_type_service

router = APIRouter(
    prefix="/candidate_stage_type",
    tags=["CandidateStageType"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[CandidateStageTypeRead],
            summary="Get all CandidateStageType")
async def get_all(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        Authorize: AuthJWT = Depends()
):
    """
        Get all Candidates.

        - **skip**: int - The number of badges to skip before returning the results. This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of badges to return in the response. This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return candidate_stage_type_service.get_multi(db, skip, limit)


@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateStageTypeRead,
            summary="Get a CandidateStageType by id")
async def get_by_id(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None
):
    """
        Get a CandidateStageType by id.

        - **id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    return candidate_stage_type_service.get_by_id(db, id)


@router.post("", dependencies=[Depends(HTTPBearer())],
             status_code=status.HTTP_201_CREATED,
             summary="Create a CandidateStageType",
             response_model=CandidateStageTypeRead)
async def create(
        db: Session = Depends(get_db),
        body: CandidateStageTypeCreate = None,
        Authorize: AuthJWT = Depends()
):
    """
        Create a CandidateStageType.

        - **name**: str - required
    """
    Authorize.jwt_required()
    return candidate_stage_type_service.create(db, body)


@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
            response_model=CandidateStageTypeRead,
            summary="Update a CandidateStageType")
async def update(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None,
        body: CandidateStageTypeUpdate = None
):
    """
        Update a CandidateStageType.

        - **id**: UUID - required and should exist in the database.
        - **name**: str - required
    """
    Authorize.jwt_required()
    return candidate_stage_type_service.update(db,
                                               db_obj=candidate_stage_type_service.get_by_id(
                                                   db, id),
                                               obj_in=body)


@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a CandidateStageType")
async def delete(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
        id: uuid.UUID = None
):
    """
        Delete a CandidateStageType.

        - **id**: UUID - required and should exist in the database.
    """
    Authorize.jwt_required()
    candidate_stage_type_service.remove(db, id)
