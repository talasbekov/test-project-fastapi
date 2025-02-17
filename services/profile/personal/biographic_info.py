from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import BiographicInfo, Birthplace
from models.personal import PersonalProfile
from schemas import BiographicInfoCreate, BiographicInfoUpdate, BirthplaceCreate
from services.base import ServiceBase
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException


class BiographicInfoService(ServiceBase[BiographicInfo, BiographicInfoCreate, BiographicInfoUpdate]):

    def get_by_id(self, db: Session, id: str):
        biographic_info = super().get(db, id)
        # biographic_info = db.query(self.model).filter(
        #     self.model.id == id).first()
        if biographic_info is None:
            raise NotFoundException(
                detail=f"BiographicInfo with id: {id} is not found!")
        return biographic_info
    
    def get_by_user_id(self, db: Session, user_id: str):
        user_id = user_id.lower() 
        biographic_info = db.query(self.model).filter(
            self.model.user_id == user_id).first()
        if not biographic_info:
            raise NotFoundException(
                detail=f"Biographic info with user_id: {user_id} is not found!")
        return biographic_info

    def get_by_profile_id(self, db: Session, profile_id: str):
        biographic_info = db.query(self.model).filter(
            self.model.profile_id == profile_id).first()
        if not biographic_info:
            raise NotFoundException(
                detail=f"Biographic info with id: {profile_id} is not found!")
        return biographic_info

    def create(self, db: Session, biographic_info: BiographicInfoCreate):
        # find birthplace if it exists
        birthplace = db.query(Birthplace).filter(Birthplace.city_id == biographic_info.city_id, Birthplace.country_id==biographic_info.country_id, Birthplace.region_id==biographic_info.region_id).first()
        if not birthplace:
            birthplace = Birthplace(
                region_id=biographic_info.region_id,
                city_id=biographic_info.city_id,
                country_id=biographic_info.country_id
            )            
            db.add(birthplace)
            db.flush()
        
        profiles = db.query(PersonalProfile).filter(
            PersonalProfile.profile_id == biographic_info.personal_profile_id
        ).all()
        if not profiles:
            raise HTTPException(status_code=400, detail="Profile ID not found in hr_erp_personal_profiles.")
        profile = profiles[0]

        biographic_info_new = self.model(
            birthplace_id = birthplace.id,
            gender = biographic_info.gender,
            address = biographic_info.address,
            family_status_id = biographic_info.family_status_id,
            residence_address = biographic_info.residence_address,
            profile_id = profile.id,
            personal_profile_id = biographic_info.personal_profile_id,
            citizenship_id = biographic_info.citizenship_id,
            nationality_id = biographic_info.nationality_id,
        )
        db.add(biographic_info_new)
        db.flush()
        return biographic_info_new
    
    def update(self, db: Session, id: str, biographic_info: BiographicInfoUpdate) -> BiographicInfo:
        biographic_info_new = self.get_by_id(db, id)
        # find birthplace if it exists
        birthplace = db.query(Birthplace).filter(Birthplace.city_id == biographic_info.city_id, Birthplace.country_id==biographic_info.country_id, Birthplace.region_id==biographic_info.region_id).first()
        if not birthplace:
            birthplace = Birthplace(
                region_id=biographic_info.region_id,
                city_id=biographic_info.city_id,
                country_id=biographic_info.country_id
            )            
            db.add(birthplace)
            db.flush()
        biographic_info_new.birthplace_id = birthplace.id
        biographic_info_new.gender = biographic_info.gender
        biographic_info_new.address = biographic_info.address
        biographic_info_new.family_status_id = biographic_info.family_status_id
        biographic_info_new.residence_address = biographic_info.residence_address
        biographic_info_new.profile_id = biographic_info.profile_id
        biographic_info_new.citizenship_id = biographic_info.citizenship_id
        biographic_info_new.nationality_id = biographic_info.nationality_id
        db.add(biographic_info_new)
        db.flush()
        return biographic_info_new

biographic_info_service = BiographicInfoService(BiographicInfo)
