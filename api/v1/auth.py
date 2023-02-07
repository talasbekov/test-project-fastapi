from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from schemas import LoginForm
from core import get_db, configs

router = APIRouter(prefix="/auth", tags=["Authorization"])
