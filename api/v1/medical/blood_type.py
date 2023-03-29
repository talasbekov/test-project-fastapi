from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import BloodType

router = APIRouter(prefix="/blood_types", tags=["BloodType"], dependencies=[Depends(HTTPBearer())])


@router.get("")
async def get_all(*,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return [bt.value for bt in BloodType]
