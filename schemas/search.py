from typing import List, Optional
from schemas import Model


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


class Search(Model):
    user_id: Optional[str] = None
    name: Optional[str] = None


class SearchType(Model):
    search_type: str
    name: str

class SearchTypeListCreate(Model):
    search_types: List[SearchType]


class SearchTypeListRead(Model):
    users: List[Search]