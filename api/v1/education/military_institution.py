import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import MilitaryInstitutionCreate, MilitaryInstitutionUpdate, MilitaryInstitutionRead, MilitaryInstitutionReadPagination
from services import military_institution_service


router = APIRouter(
    prefix="/military_institution",
    tags=["MilitaryInstitution"],
    dependencies=[
        Depends(
            HTTPBearer())])

@router.get("", dependencies=[Depends(HTTPBearer())],
                response_model=MilitaryInstitutionReadPagination,
                summary="Get all MilitaryInstitution")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all MilitaryInstitution

        - **skip**: int - The number of MilitaryInstitution
            to skip before returning the results.
            This parameter is optional and defaults to 0.
        - **limit**: int - The maximum number of MilitaryInstitution
            to return in the response.
            This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    return military_institution_service.get_all(db, skip, limit)

@router.post("", status_code=status.HTTP_201_CREATED,
                dependencies=[Depends(HTTPBearer())],
                response_model=MilitaryInstitutionRead,
                summary="Create MilitaryInstitution")
async def create(*,
                db: Session = Depends(get_db),
                body: MilitaryInstitutionCreate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Create new MilitaryInstitution
    """
    Authorize.jwt_required()
    return military_institution_service.create(db, body)

@router.get("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=MilitaryInstitutionRead,
                summary="Get MilitaryInstitution by ID")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get MilitaryInstitution by ID
    """
    Authorize.jwt_required()
    return military_institution_service.get_by_id(db, id)

@router.put("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=MilitaryInstitutionRead,
                summary="Update MilitaryInstitution by ID")
async def update(*,
                db: Session = Depends(get_db),
                id: str,
                body: MilitaryInstitutionUpdate,
                Authorize: AuthJWT = Depends()
                ):
    """
        Update MilitaryInstitution by ID
    """
    Authorize.jwt_required()
    MilitaryInstitution = military_institution_service.get_by_id(db, id)
    return military_institution_service.update(db, db_obj=MilitaryInstitution, obj_in=body)

@router.delete("/{id}", dependencies=[Depends(HTTPBearer())],
                response_model=MilitaryInstitutionRead,
                summary="Delete MilitaryInstitution by ID")
async def delete(*,
                db: Session = Depends(get_db),
                id: str,
                Authorize: AuthJWT = Depends()
                ):
    """
        Delete MilitaryInstitution by ID
    """
    Authorize.jwt_required()
    return military_institution_service.remove(db, id)
