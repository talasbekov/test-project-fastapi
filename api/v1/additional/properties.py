import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import PropertiesCreate, PropertiesRead, PropertiesUpdate
from services import properties_service, profile_service

router = APIRouter(
    prefix="/properties",
    tags=["Properties"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[PropertiesRead],
            summary="Get all Properties")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Properties

    - **skip**: int - The number of Propertiers to skip before returning the results.
        This parameter is optional and defaults to 0.
    - **limit**: int - The maximum number of Properties to return in the response.
        This parameter is optional and defaults to 100.
    """
    Authorize.jwt_required()
    credentials = Authorize.get_jwt_subject()
    return properties_service.get_multi_by_user_id(
        db, credentials, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=PropertiesRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 body: PropertiesCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new abroad travel

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    return properties_service.create(db, body)


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PropertiesRead,
            summary="Update property by id")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: PropertiesUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update property by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    property = properties_service.get_by_id(db, str(id))
    return properties_service.update(db=db, db_obj=property, obj_in=body)


@router.delete("/{id}/", dependencies=[Depends(HTTPBearer())],
               response_model=PropertiesRead,
               summary="Delete properties by id")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete properties by id

        - **name**: required
        - **url**: image url. This parameter is required
    """
    Authorize.jwt_required()
    properties = properties_service.get_by_id(db, str(id))
    return properties_service.remove(db=db, id=properties.id)
