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

@router.post("/login", summary="Login")
async def login(form: LoginForm, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """
    Login to the system.

    - **email**: required and should be a valid email format.
    - **password**: required.
    """
    return auth_service.login(form, db, Authorize)


@router.post("/register", summary="Register")
async def register(form: RegistrationForm, db: Session = Depends(get_db)):
    """
        Register new user to the system.

        - **email**: string required and should be a valid email format.
        - **first_name**: required.
        - **last_name**: required.
        - **father_name**: optional.
        - **group_id**: UUID - required and should exist in the database
        - **position_id**: UUID - required and should exist in the database.
        - **icon**: image with url format. This parameter is optional.
        - **call_sign**: required.
        - **id_number**: unique employee number. This parameter is required.
        - **phone_number**: format (+77xxxxxxxxx). This parameter is optional.
        - **address**: optional.
        - **birthday**: format (YYYY-MM-DD). This parameter is optional.
        - **status**: the current status of the employee (e.g. "working", "on vacation", "sick", etc.). This parameter is optional.
        - **status_till**: the date when the current status of the employee will end. This parameter is optional.
        - **role_name**: required.
        - **password**: required.
        - **re_password**: required and should match the password field.
    """
    return auth_service.register(form, db)

@router.get('/refresh', dependencies=[Depends(HTTPBearer())])
def refresh_token(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    return auth_service.refresh_token(db, Authorize)
