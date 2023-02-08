from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from schemas import LoginForm, RegistrationForm, UserRead
from core import get_db, configs
from services import auth_service, user_service

router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/login")
async def login(form: LoginForm, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth_service.login(form, db, Authorize)


@router.post("/register", response_model=UserRead)
async def register(form: RegistrationForm, db: Session = Depends(get_db)):
    return auth_service.register(form, db)


@router.get('/refresh', dependencies=[Depends(HTTPBearer())])
def refresh_token(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    user = user_service.get(db, Authorize.get_jwt_subject())
    if not Authorize.get_jwt_subject():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='The user belonging to this token no logger exist')

    current_user_id=Authorize.get_jwt_subject()
    user_claims = {
        "role": user.role.name
    }
    access_token=Authorize.create_access_token(subject=current_user_id, user_claims=user_claims, expires_time=timedelta(minutes=configs.ACCESS_TOKEN_EXPIRES_IN))
    refresh_token = Authorize.create_refresh_token(subject=current_user_id, user_claims=user_claims, expires_time=timedelta(minutes=configs.REFRESH_TOKEN_EXPIRES_IN))

    return {"new_access_token": access_token, "refresh_token": refresh_token}
