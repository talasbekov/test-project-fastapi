from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log
from fastapi import HTTPException, status
from datetime import timedelta
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from core import configs

from schemas import LoginForm, RegistrationForm, UserCreate

from services import user_service, group_service
from exceptions import BadRequestException
from utils import verify_password, hash_password, is_valid_phone_number


class AuthService():
    
    def login(self, form: LoginForm, db: Session, Authorize: AuthJWT):
        user = user_service.get_by_email(db, EmailStr(form.email).lower())

        if not user:
            raise BadRequestException(detail="Incorrect email or password!")
        if not verify_password(form.password, user.password):
            raise BadRequestException(detail='Incorrect email or password')
        
        user_claims = {
            "role": user.position
        }
        access_token = Authorize.create_access_token(
            subject=str(user.id), user_claims=user_claims, expires_time=timedelta(minutes=configs.ACCESS_TOKEN_EXPIRES_IN)
        )
        refresh_token = Authorize.create_refresh_token(
            subject=str(user.id), user_claims=user_claims, expires_time=timedelta(minutes=configs.REFRESH_TOKEN_EXPIRES_IN)
        )

        return {"access_token": access_token, "refresh_token": refresh_token}
    
    def register(self, form: RegistrationForm, db: Session):
        user_obj = user_service.get_by_email(db, EmailStr(form.email).lower())
        group_obj = group_service.get_by_id(db, form.group_id)
        
        if user_obj:
            raise HTTPException(status_code=400, detail="User with this email already exists!")
        if not is_valid_phone_number(form.phone_number):
            raise HTTPException(status_code=400, detail="Invalid phone number!")
        if form.password != form.re_password:
            raise HTTPException(status_code=400, detail="Password mismatch!")

        user_obj_in = UserCreate(
            email=EmailStr(form.email).lower(),
            first_name=form.first_name,
            last_name=form.last_name,
            phone_number=form.phone_number,
            password=hash_password(form.password),
            middle_name=form.middle_name,
            group_id=group_obj.id,
            call_sign=form.call_sign,
            id_number=form.id_number,
            address=form.address,
            birthday=form.birthday
        )

        return user_service.create(db, user_obj_in)


auth_service = AuthService()
