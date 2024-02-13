from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import ServiceIDStatus
from schemas import ServiceIDCreate, ServiceIDRead, ServiceIDUpdate
from services import service_id_service

router = APIRouter(
    prefix="/service_id",
    tags=["ServiceID"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[ServiceIDRead],
            summary="Get all ServiceID")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Profiles

    """
    Authorize.jwt_required()
    return service_id_service.get_multi(db, skip=skip, limit=limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=ServiceIDRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: ServiceIDCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new ServiceID

        no parameters required.
    """
    Authorize.jwt_required()
    return service_id_service.create(db, obj_in=body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ServiceIDRead,
            summary="Get ServiceID by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get ServiceID by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return service_id_service.get_by_id(db, id=id)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=ServiceIDRead,
            summary="Update ServiceID")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: ServiceIDUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update ServiceID

    """
    Authorize.jwt_required()
    service_id = service_id_service.get_by_id(db, str(id))
    return service_id_service.update(db, db_obj=service_id, obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete ServiceID")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Profile

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    service_id_service.remove(db, id=id)


@router.get("statuses/", dependencies=[Depends(HTTPBearer())],
            response_model=List[dict],
            summary="Get all ServiceID statuses")
async def get_all_statuses(
):
    """
        Get all ServiceID statuses

    """
    statuses = []
    for status in ServiceIDStatus:
        statuses.append({'name': status.name,
                         'value': status.value})
    return statuses
