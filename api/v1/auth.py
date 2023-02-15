from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from schemas import LoginForm, RegistrationForm, UserRead
from core import get_db, configs
from services import auth_service, user_service
from exceptions import SgoErpException

router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/login")
async def login(form: LoginForm, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth_service.login(form, db, Authorize)


@router.post("/register", response_model=UserRead)
async def register(form: RegistrationForm, db: Session = Depends(get_db)):
    try:
        created_user = auth_service.register(form, db)
        db.commit()
        return created_user
    except HTTPException as e:
        db.rollback()
        raise e


@router.get('/refresh', dependencies=[Depends(HTTPBearer())])
def refresh_token(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    return auth_service.refresh_token(db, Authorize)
