from typing import List
import json

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from schemas import (NotificationRead, DetailedNotificationRead,
                     DetailedNotificationCreate, NotificationCreate,
                     DetailedNotificationReadPagination,
                     NotificationReadPagination)
from services import notification_service, detailed_notification_service

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    dependencies=[
        Depends(
            HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=NotificationReadPagination,
            summary="Get all Notifications")
async def get_all(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    """
       Get all Notifications

       - **skip**: int - The number of Notifications
        to skip before returning the results.
        This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of Notifications
        to return in the response.
        This parameter is optional and defaults to 10.
   """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return notification_service.get_receiveds_by_user_id(
        db, user_id, skip, limit)
    
@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=NotificationRead,
             summary="Create Notification")
async def create(*,
                 db: Session = Depends(get_db),
                 body: NotificationCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Notification

        **name** - required - str
    """
    Authorize.jwt_required()
    return notification_service.create(db, body)

@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Notification")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Notification

        - **id** - UUID - required
    """
    Authorize.jwt_required()
    notification_service.remove(db, str(id))

    
@router.get("/test", dependencies=[Depends(HTTPBearer())],
            summary="Test Notifications")
async def test(*,
               db: Session = Depends(get_db),
               Authorize: AuthJWT = Depends(),
               message: str = 'anime',
               ):
    """
       Test all Notifications
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    message = {
        "sender_type": "test",
        "message": message
    }
    return await notification_service.send_message(db, message, user_id)

@router.get("/detailed", dependencies=[Depends(HTTPBearer())],
            response_model=DetailedNotificationReadPagination,
            summary="Get all Detailed Notifications")
async def get_all_detailed(*,
                  db: Session = Depends(get_db),
                  Authorize: AuthJWT = Depends(),
                  skip: int = 0,
                  limit: int = 10
                  ):
    """
       Get all Detailed Notifications

       - **skip**: int - The number of Notifications
        to skip before returning the results.
        This parameter is optional and defaults to 0.
       - **limit**: int - The maximum number of Notifications
        to return in the response.
        This parameter is optional and defaults to 10.
   """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return detailed_notification_service.get_multi(db, user_id, skip, limit)

@router.post("/detailed", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=DetailedNotificationRead,
             summary="Create Detailed Notification")
async def create(*,
                 db: Session = Depends(get_db),
                 body: DetailedNotificationCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Detailed Notifications

        **name** - required - str
    """
    Authorize.jwt_required()
    return detailed_notification_service.create(db, body)