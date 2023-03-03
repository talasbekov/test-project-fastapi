from datetime import timedelta

from fastapi import HTTPException, status
from fastapi.logger import logger as log
from fastapi_jwt_auth import AuthJWT
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core import configs
from exceptions import BadRequestException
from models import User
from schemas import LoginForm, RegistrationForm, UserCreate
from services import staff_division_service, staff_unit_service, user_service
from utils import hash_password, is_valid_phone_number, verify_password


class AuthService():
    
    def login(self, form: LoginForm, db: Session, Authorize: AuthJWT):
        user = user_service.get_by_email(db, EmailStr(form.email).lower())

        if not user:
            raise BadRequestException(detail="Incorrect email or password!")
        if not verify_password(form.password, user.password):
            raise BadRequestException(detail='Incorrect email or password')
        
        access_token, refresh_token = self._generate_tokens(Authorize, user)

        return {"access_token": access_token, "refresh_token": refresh_token}
    
    def register(self, form: RegistrationForm, db: Session):
        group_obj = staff_division_service.get_by_id(db, form.group_id)
        position_obj = staff_unit_service.get_by_id(db, form.position_id)

        if user_service.get_by_email(db, EmailStr(form.email).lower()):
            raise BadRequestException(detail="User with this email already exists!")
        if user_service.get_by_call_sign(db, form.call_sign):
            raise BadRequestException(detail="User with this call_sign already exists!")
        if user_service.get_by_id_number(db, form.id_number):
            raise BadRequestException(detail="User with this id_number already exists!")
        if not is_valid_phone_number(form.phone_number):
            raise BadRequestException(detail="Invalid phone number!")
        if form.password != form.re_password:
            raise BadRequestException(detail="Password mismatch!")

        user_obj_in = UserCreate(
            email=EmailStr(form.email).lower(),
            first_name=form.first_name,
            last_name=form.last_name,
            phone_number=form.phone_number,
            password=hash_password(form.password),
            father_name=form.father_name,
            position_id=position_obj.id,
            group_id=group_obj.id,
            call_sign=form.call_sign,
            id_number=form.id_number,
            address=form.address,
            birthday=form.birthday
        )

        return user_service.create(db, user_obj_in)
    
    def refresh_token(self, db: Session, Authorize: AuthJWT):
        if not Authorize.get_jwt_subject():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Could not refresh access token')
        user = user_service.get(db, Authorize.get_jwt_subject())
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no longer exist')
        
        access_token, refresh_token = self._generate_tokens(Authorize, user)

        return {"access_token": access_token, "refresh_token": refresh_token}

    
    def _generate_tokens(self, Authorize: AuthJWT, user: User):

        user_claims = {
            "role": str(user.actual_staff_unit.id)
        }
        access_token = Authorize.create_access_token(
            subject=str(user.id),
            user_claims=user_claims,
            expires_time=timedelta(minutes=configs.ACCESS_TOKEN_EXPIRES_IN)
        )
        refresh_token = Authorize.create_refresh_token(
            subject=str(user.id),
            user_claims=user_claims,
            expires_time=timedelta(minutes=configs.REFRESH_TOKEN_EXPIRES_IN)
        )

        return access_token, refresh_token


auth_service = AuthService()
