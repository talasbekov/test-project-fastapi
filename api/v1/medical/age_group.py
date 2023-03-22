from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import AgeGroup

router = APIRouter(prefix="/age_group", tags=["AgeGroup"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            summary="Get all AgeGroup")
async def get_all(*,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
        Get all AgeGroupEnum

    """
    Authorize.jwt_required()
    return [ag.value for ag in AgeGroup]
