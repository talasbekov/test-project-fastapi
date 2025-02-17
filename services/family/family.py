from typing import List
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Family, Birthplace, FamilyProfile
from schemas import FamilyCreate, FamilyUpdate
from services import ServiceBase, violation_service, abroad_travel_service
from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from models.association import family_violation, family_abroad_travel
from sqlalchemy import insert
from utils.date import parse_datetime
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException
from uuid import UUID


class FamilyService(ServiceBase[Family, FamilyCreate, FamilyUpdate]):
    def get_multi(self, db: Session, skip: int = 0,
                  limit: int = 100) -> List[Family]:
        return (db.query(Family).order_by(Family.profile_id).join(Family.violation).join(Family.abroad_travel).offset(skip).limit(limit).all())

    def get_by_id(self, db: Session, id: str) -> Family:
        family = db.query(Family).outerjoin(
            Family.violation).outerjoin(
            Family.abroad_travel).filter(
            Family.id == id).first()
        if not family:
            raise NotFoundException(f"Family with id: {id} not found!")
        return family

    def get_by_relation_id(self, db: Session, relation_id: str):
        family = db.query(Family).filter(
            Family.relation_id == relation_id).first()
        return family

    def create(self, db: Session,
               obj_in: Union[FamilyCreate, Dict[str, Any]]) -> Family:
        obj_in_data = jsonable_encoder(obj_in)

        try:
            families_profile = db.query(FamilyProfile).filter(FamilyProfile.profile_id == obj_in_data['profile_id']).one()
            obj_in_data['families_profile_id'] = families_profile.id 
        except NoResultFound:
            raise HTTPException(status_code=400, detail="Profile ID not found in hr_erp_family_profiles.")

        obj_in_data['birthday'] = parse_datetime(
            obj_in_data['birthday'])
        if obj_in_data['death_day'] is not None:
            obj_in_data['death_day'] = parse_datetime(
                obj_in_data['death_day'])

        birthplace = db.query(Birthplace).filter(Birthplace.city_id == obj_in.city_id, Birthplace.country_id==obj_in.country_id, Birthplace.region_id==obj_in.region_id).first()
        if not birthplace:
            birthplace = Birthplace(
                region_id=obj_in.region_id,
                city_id=obj_in.city_id,
                country_id=obj_in.country_id
            )            
            db.add(birthplace)
            db.flush()
        
        obj_in_data['birthplace_id'] = birthplace.id
        db_obj = self.model(
            relation_id=obj_in_data['relation_id'],
            first_name=obj_in_data['first_name'],
            last_name=obj_in_data['last_name'],
            father_name=obj_in_data['father_name'],
            IIN=obj_in_data['IIN'],
            birthday=obj_in_data['birthday'],
            death_day=obj_in_data['death_day'],
            address=obj_in_data['address'],
            workplace=obj_in_data['workplace'],
            birthplace_id=obj_in_data['birthplace_id'],
            profile_id=obj_in_data['families_profile_id'],
            families_profile_id=obj_in_data['families_profile_id']
        )
        db.add(db_obj)
        db.flush()
        return db_obj
    
    def update(self, db: Session, id: str, obj_in: Union[FamilyUpdate, Dict[str, Any]]) -> Family:
        obj = self.get_by_id(db, id)
        birthplace = db.query(Birthplace).filter(Birthplace.city_id == obj_in.city_id, Birthplace.country_id==obj_in.country_id, Birthplace.region_id==obj_in.region_id).first()
        if not birthplace:
            birthplace = Birthplace(
                region_id=obj_in.region_id,
                city_id=obj_in.city_id,
                country_id=obj_in.country_id
            )            
            db.add(birthplace)
            db.flush()

        try:
            families_profile_id = db.query(FamilyProfile).filter(FamilyProfile.profile_id == obj_in.profile_id).one()
            obj.families_profile_id = families_profile_id.id 
        except NoResultFound:
            raise HTTPException(status_code=400, detail="Profile ID not found in hr_erp_family_profiles.")

        
        obj.relation_id = obj_in.relation_id
        obj.first_name = obj_in.first_name
        obj.last_name = obj_in.last_name
        obj.father_name = obj_in.father_name
        obj.IIN = obj_in.IIN
        obj.birthday = obj_in.birthday
        obj.death_day = obj_in.death_day
        obj.address = obj_in.address
        obj.workplace = obj_in.workplace
        obj.birthplace_id = birthplace.id
        obj.profile_id = families_profile_id.id
        db.add(obj)
        db.flush()
        return obj

    def create_violation(self, db: Session, family_id: str,
                         obj_in):
        # set profile_id in obj_in
        # obj_in['profile_id'] = None
        violation = violation_service.create_family_violation(db, obj_in)
        # print(violation.id)
        family = self.get_by_id(db, family_id)
        stmt = insert(family_violation).values(family_id=family.id, violation_id=violation.id)
        db.execute(stmt)

        return family

    def create_abroad_travel(self, db: Session, family_id: str,
                             obj_in):
        # set profile_id in obj_in
        # obj_in['profile_id'] = None
        abroad_travel = abroad_travel_service.create_family_travel(db, obj_in)
        family = self.get_by_id(db, family_id)
        # family.abroad_travel.append(abroad_travel)
        stmt = insert(family_abroad_travel).values(family_id=family.id, abroad_travel_id=abroad_travel.id)
        db.execute(stmt)
        return family

    def remove(self, db: Session, id: str) -> Family:
        obj = db.query(self.model).get(id)
        obj.violation = []
        obj.abroad_travel = []
        db.delete(obj)
        db.flush()
        return obj


family_service = FamilyService(Family)
