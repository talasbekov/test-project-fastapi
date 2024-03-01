import datetime
from typing import Optional

from schemas import NamedModel, ReadNamedModel
from schemas import UserRead

class LiveSearchBase(NamedModel):
    user_name: Optional[str]
    user_last_name: Optional[str]
    user_father_name: Optional[str]
    user_call_sign: Optional[str]
    user_age: Optional[int]
    user_iin: Optional[str]
    user_phone_number: Optional[str]
    user_cabinet: Optional[str]
    user_service_phone_number: Optional[str]
    user_personal_id: Optional[str]
    user_id_number: Optional[str]
    user_supervised_by: Optional[str]
    position_id: Optional[str]
    rank_type_id: Optional[str]
    badge_type_id: Optional[str]
    staff_division_id: Optional[str]
    biographic_info_gender: Optional[bool]
    biographic_info_citizenship: Optional[str]
    biographic_info_nationality: Optional[str]
    biographic_info_address: Optional[str]
    biographic_info_residence_address: Optional[str]
    biographic_info_place_birth: Optional[str]
    has_driving_license: Optional[bool]
    driving_license_category_code: Optional[bool]
    has_id_card: Optional[bool]
    has_passport: Optional[bool]
    has_financial_info: Optional[bool]
    sport_degree_type_id: Optional[str]
    sport_degree_degree_id: Optional[str]
    sport_achievement_id: Optional[str]
    sport_achievement_type_id: Optional[str]
    academic_degree_degree_id: Optional[str]
    science_id: Optional[str]
    specialty_id: Optional[str]
    academic_title_degree_id: Optional[str]
    course_provider_id: Optional[str]
    course_id: Optional[str]
    institution_id: Optional[str]
    institution_degree_id: Optional[str]
    language_id: Optional[str]
    language_proficiency_id: Optional[str]
    oath_military_name: Optional[str]
    personal_reserve_name_with_document_number: Optional[str]
    has_black_beret: Optional[bool]
    coolness_type_id: Optional[str]
    coolness_status_name: Optional[str]
    recommendant_name: Optional[str]
    researcher_name: Optional[str]

    date_from: Optional[datetime.date]
    date_to: Optional[datetime.date]


class LiveSearchCreate(LiveSearchBase):
    pass


class LiveSearchUpdate(LiveSearchBase):
    pass


class LiveSearchRead(LiveSearchBase, ReadNamedModel):

    class Config:
        orm_mode = True
