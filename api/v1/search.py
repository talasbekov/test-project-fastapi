from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db  
from schemas.search import SearchType, SearchTypeListCreate, SearchTypeListRead, Search
from services.search import search_service

router = APIRouter(
    prefix="/search",
    tags=["search"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.post("", dependencies=[Depends(HTTPBearer())],
            response_model=SearchTypeListRead,
            summary="Get all ServiceID")
async def get_all(*,
                  searches_params: SearchTypeListCreate,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Profiles

    """ 
    Authorize.jwt_required() 
    info = await search_service.general(db=db, params=searches_params, skip=skip, limit=limit)
    print(info)
    return info

