from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import HexagonAveragesRead, HexagonRead
from services import hexagon_service

router = APIRouter(
    prefix="/hexagon",
    tags=["Hexagon"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=HexagonRead,
            summary="Get last hexagon")
async def get_last_hexagon(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get last hexagon
   """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hexagon_service.get_by_user_id(db, user_id)

@router.get("/average", dependencies=[Depends(HTTPBearer())],
            response_model=HexagonAveragesRead,
            summary="Get average scores for hexagon")
async def get_last_hexagon(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get average scores for hexagon
    """
    Authorize.jwt_required()
    return hexagon_service.get_average(db)


@router.get("/date", dependencies=[Depends(HTTPBearer())],
            response_model=List[HexagonRead],
            summary="Get hexagons by date")
async def get_last_hexagon(*,
                  db: Session = Depends(get_db),
                  date_from: datetime,
                  Authorize: AuthJWT = Depends()
                  ):
    """
       Get hexagons by date
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return hexagon_service.get_by_user_id_and_date(db, user_id, date_from)