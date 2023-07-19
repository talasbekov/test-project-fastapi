import random

from datetime import timedelta, datetime

from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core import configs
from exceptions import BadRequestException
from models import User, StaffDivisionEnum, StaffUnit
from schemas import (
    LoginForm,
    RegistrationForm,
    UserCreate,
    ProfileCreate,
    EducationalProfileCreate,
    AdditionalProfileCreate,
    PersonalProfileCreate,
    MedicalProfileCreate,
    FamilyProfileCreate,
    CandidateRegistrationForm,
    StaffUnitCreate,
    CandidateCreate
)
from services import (
    staff_unit_service,
    user_service,
    profile_service,
    educational_profile_service,
    additional_profile_service,
    personal_profile_service,
    medical_profile_service,
    family_profile_service,
    staff_division_service,
    candidate_service,
    user_logging_activity_service
)
from utils import hash_password, is_valid_phone_number, verify_password


class AuthService():

    def login(self, form: LoginForm, db: Session, Authorize: AuthJWT):
        user = user_service.get_by_email(db, EmailStr(form.email).lower())

        if not user:
            raise BadRequestException(detail="Incorrect email or password!")
        if not verify_password(form.password, user.password):
            raise BadRequestException(detail='Incorrect email or password')

        self._set_last_signed_at(db, user)

        access_token, refresh_token = self._generate_tokens(Authorize, user)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def register(self, form: RegistrationForm, db: Session):

        if user_service.get_by_email(db, EmailStr(form.email).lower()):
            raise BadRequestException(
                detail="User with this email already exists!")
        if user_service.get_by_call_sign(db, form.call_sign):
            raise BadRequestException(
                detail="User with this call_sign already exists!")
        if user_service.get_by_id_number(db, form.id_number):
            raise BadRequestException(
                detail="User with this id_number already exists!")
        if not is_valid_phone_number(form.phone_number):
            raise BadRequestException(detail="Invalid phone number!")
        if form.password != form.re_password:
            raise BadRequestException(detail="Password mismatch!")

        user_obj_in = UserCreate(
            email=EmailStr(form.email).lower(),
            first_name=form.first_name,
            last_name=form.last_name,
            father_name=form.father_name,
            staff_unit_id=form.staff_unit_id,
            actual_staff_unit_id=form.actual_staff_unit_id,
            icon=form.icon,
            call_sign=form.call_sign,
            id_number=form.id_number,
            phone_number=form.phone_number,
            address=form.address,
            cabinet=form.cabinet,
            service_phone_number=form.service_phone_number,
            supervised_by=None,
            is_military=form.is_military,
            personal_id=form.personal_id,
            date_birth=form.date_birth,
            iin=form.iin,
            password=hash_password(form.password),
            is_active=True
        )

        user = user_service.create(db=db, obj_in=user_obj_in)

        self._create_profiles(db, user.id)

        return user

    def register_candidate(
            self, form: CandidateRegistrationForm, db: Session, staff_unit_id: str):

        if user_service.get_by_iin(db, form.iin):
            raise BadRequestException(
                detail="User with this iin already exists!")

        birth_date = self._extract_birth_date_from_iin(form.iin)

        # Get current user and staff unit
        current_user_staff_unit: StaffUnit = staff_unit_service.get_by_id(
            db, staff_unit_id)
        current_user: User = current_user_staff_unit.actual_users[0]

        # Create new staff unit for candidate
        special_candidate_group = staff_division_service.get_by_name(
            db, StaffDivisionEnum.CANDIDATES.value)
        staff_unit = staff_unit_service.create(db, obj_in=StaffUnitCreate(
            position_id=current_user_staff_unit.position_id,
            staff_division_id=special_candidate_group.id
        ))

        # Generate fake personal information for candidate
        first_names = [
            "Канат",
            "Мади",
            "Алибек",
            "Абдулла",
            "Аскар",
            "Хабдулла",
            "Азамат",
            "Бахыт",
            "Дамир",
            "Дастан"]
        last_names = [
            "Алибеков",
            "Қанатов",
            "Қенжебаев",
            "Құдайбергенов",
            "Нұрғалиев",
            "Омаров",
            "Оспанов",
            "Султанов",
            "Турсынбаев",
            "Жақыпов"]
        father_names = [
            "Әбдулович",
            "Айбекович",
            "Әлишерович",
            "Әрманович",
            "Бекзатович",
            "Дәулетович",
            "Нұрлыбекович",
            "Русланович",
            "Санжарович",
            "Ержанович"]

        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        father_name = random.choice(father_names)

        random_int = random.randint(10000000, 99999999)
        # concatenate random int to call_sign
        call_sign = f"{current_user.call_sign}{random_int}"
        # concatenate random int to id_number
        id_number = f"{current_user.id_number}{random_int}"

        # Create new user and candidate
        user_obj_in = UserCreate(
            email=None,
            first_name=first_name,
            last_name=last_name,
            father_name=father_name,
            staff_unit_id=staff_unit.id,
            actual_staff_unit_id=staff_unit.id,
            icon=current_user.icon,
            call_sign=call_sign,
            id_number=id_number,
            phone_number=current_user.phone_number,
            address=current_user.address,
            cabinet=None,
            service_phone_number=None,
            supervised_by=current_user.id,
            is_military=None,
            personal_id=None,
            date_birth=birth_date,
            iin=form.iin,
            password=None,
            is_active=True
        )

        user = user_service.create(db=db, obj_in=user_obj_in)

        candidate_service.create(db, body=CandidateCreate(
            staff_unit_curator_id=current_user_staff_unit.id,
            staff_unit_id=staff_unit.id
        ))

        self._create_profiles(db, user.id)

        return user

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
            "role": str(user.staff_unit.id),
            "iin": str(user.iin)
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

    def _create_profiles(self, db: Session, user_id: str):
        profile = profile_service.create(db=db, obj_in=ProfileCreate(
            user_id=user_id
        ))

        educational_profile_service.create(db=db, obj_in=EducationalProfileCreate(
            profile_id=profile.id
        ))

        additional_profile_service.create(db=db, obj_in=AdditionalProfileCreate(
            profile_id=profile.id
        ))

        personal_profile_service.create(db=db, obj_in=PersonalProfileCreate(
            profile_id=profile.id
        ))

        medical_profile_service.create(db=db, obj_in=MedicalProfileCreate(
            profile_id=profile.id
        ))

        family_profile_service.create(db=db, obj_in=FamilyProfileCreate(
            profile_id=profile.id
        ))

    def _set_last_signed_at(self, db: Session, user: User):
        user.last_signed_at = datetime.now()
        
        user_logging_activity_service.create(db, user.id)

        db.add(user)
        db.flush()

    def _extract_birth_date_from_iin(self, iin: str):
        try:
            date_str = iin[:6]
            birth_date = datetime.strptime(date_str, '%y%m%d')
        except ValueError:
            raise BadRequestException(detail="Invalid date in iin parameter!")

        # ensure date of birth is in the past
        if birth_date > datetime.today():
            raise BadRequestException(
                detail="Date of birth in iin parameter is in the future!")

        return birth_date


auth_service = AuthService()
