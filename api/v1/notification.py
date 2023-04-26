import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import NotificationCreate, NotificationRead, NotificationUpdate
from services import notification_service

router = APIRouter(prefix="/notifications", tags=["Notifications"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[NotificationRead],
            summary="Get all Notifications")
async def get_all(*,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    skip: int = 0,
    limit: int = 10
):
    """
       Get all Notifications

       - **skip**: int - The number of Notifications to skip before returning the results. This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of Notifications to return in the response. This parameter is optional and defaults to 10.
   """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return notification_service.get_received_by_user_id(db, user_id, skip, limit)
