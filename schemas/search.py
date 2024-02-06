from pydantic import BaseModel
from enum import Enum
from typing import List, Optional


class SearchType:
    GENERAL = "general"
    BYOGRAPHIC = "byographic"
    IDCARD = "idcard"
    DRIVERLICENSE = "driverlicense"
    PASSPORT = "passport"
    BANKACCOUNT = "bankaccount" 
    SPORTSKILL = "sportskill"
    SPORTACHIEVEMENT = "sportachievement"
    CHANGENAME = "changename"
    EDUCATION = "education"
    COURSE = "course"
    ACADEMICDEGREE = "academicdegree"
    ACADEMICTITLE = "academictitle"
    GENERALINFO = "generalinfo"
    BADGE = "badge"
    CONTRACT = "contract"
    URGENTSERVICE = "urgentservice"
    WORKEXPERIENCE = "workexperience"
    SECONDMENT = "secondment"
    ATTENDANCE = "attendance"
    AWARD = "award"
    COLLECTION = "collection"
    ATTESTATION = "attestation"
    SERVICE = "service"
    HOLLIDAY = "holliday"
    SERVICEIDCARD = "serviceidcard"
    PROPERTY = "property"
    MEDICALGENERAL = "medicalgeneral"
    ANTHROPOMETRY = "anthropometry"
    SICKLEAVE = "sickleave"
    LIBERATION = "liberation"
    DISPENSARY = "dispensary"
    FAMILY = "family"
    OFFENSES = "offenses"
    HOUSING = "housing"
    TRANSPORT = "transport"
    SERVICEHOUSING = "servicehousing"
    TRAVEL = "travel"
    SPECIALCHECK = "specialcheck"
    PSYCHOLOGICAL = "psychological"
    POLYGRAPH = "polygraph"
    STAFF_UNIT = "staff_unit"
    STAFF_DIVISION = "staff_division"


class Search(BaseModel):
    user_id: Optional[str] = None
    name: Optional[str] = None


class SearchType(BaseModel):
    search_type: str
    name: str

class SearchTypeListCreate(BaseModel):
    search_types: List[SearchType]


class SearchTypeListRead(BaseModel):
    users: List[Search]