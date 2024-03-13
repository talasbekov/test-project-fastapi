import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models.position import CategoryCodeEnum
from schemas import PositionCreate, PositionUpdate, PositionRead, PositionPaginationRead
from services import position_service, position_type_service

router = APIRouter(
    prefix="/positions",
    tags=["Positions"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=PositionPaginationRead,
            summary="Get all Positions without specials")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  filter: str = '',
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Positions without specials

       - **skip**: int - The number of Positions
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of Positions
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return position_service.get_without_special(db, skip, limit, filter)

@router.get("/all", dependencies=[Depends(HTTPBearer())],
            response_model=PositionPaginationRead,
            summary="Get all Positions")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  filter: str = '',
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get all Positions

       - **skip**: int - The number of Positions
            to skip before returning the results.
            This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of Positions
            to return in the response.
            This parameter is optional and defaults to 100.
   """
    Authorize.jwt_required()
    return position_service.get_multi(db, skip, limit, filter)

@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=PositionRead,
             summary="Create Position")
async def create(*,
                 db: Session = Depends(get_db),
                 body: PositionCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Position

        - **name**: required
    """
    Authorize.jwt_required()
    return position_service.create(db, body)

@router.get("/lower/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=List[PositionRead],
            summary="Get lower positions than position by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Position by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return position_service.get_lower_positions(db, str(id))


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=PositionRead,
            summary="Get Position by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Position by id

        - **id**: UUID - required
    """
    Authorize.jwt_required()
    return position_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            # response_model=PositionRead,
            summary="Update Position")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: PositionUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Position

        - **id**: UUID - the ID of badge to update. This is required.
        - **name**: required.
    """
    Authorize.jwt_required()
    position = position_service.get_by_id(db, str(id))
    position_type = position_type_service.get_by_id(db, position.type_id)
    return position_type_service.update(
        db,
        db_obj=position_type,
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Position")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete position

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    position_service.remove(db, str(id))


@router.get("/category_codes")
async def get_category_codes():
    return [i.value for i in CategoryCodeEnum]

@router.get('/get_short_positions')
async def get_short_positions(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return position_service.get_short_positions(db)