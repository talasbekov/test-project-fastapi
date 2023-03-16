from fastapi import APIRouter

from .education import router_education

from .hr_document import router as hr_document_router
from .document_staff_function_type import router as document_staff_function_type_router
from .document_staff_function import router as document_staff_function_router
from .service_staff_function_type import router as service_staff_function_type_router
from .service_staff_function import router as service_staff_function_router
from .staff_division import router as staff_division_router
from .hr_document_info import router as hr_document_info_router
from .hr_document_step import router as hr_document_step_router
from .hr_document_status import router as hr_document_status_router
from .hr_document_template import router as hr_document_template_router
from .user_stat import router as user_stat_router
from .staff_unit import router as staff_unit_router
from .user import router as user_router
from .auth import router as auth_router
from .equipment import router as equipment_router
from .badge import router as badge_router
from .rank import router as rank_router
from .jurisdiction import router as jurisdiction_router
from .profile import *
from .additional import *
from .medical import *
from .profile import router as profile_router
from .personal import (personal_profile_router, biographic_info_router, driving_license_router,
                       identification_card_router, passport_router, sport_achievement_router,
                       sport_degree_router, tax_declaration_router, user_financial_info_router, family_status_router)
from .family import router as family_router
from .staff_list import router as staff_list_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(hr_document_status_router)
router.include_router(hr_document_router)
router.include_router(service_staff_function_type_router)
router.include_router(service_staff_function_router)
router.include_router(document_staff_function_type_router)
router.include_router(document_staff_function_router)
router.include_router(staff_division_router)
router.include_router(hr_document_info_router)
router.include_router(hr_document_step_router)
router.include_router(hr_document_template_router)
router.include_router(user_stat_router)
router.include_router(staff_unit_router)
router.include_router(equipment_router)
router.include_router(badge_router)
router.include_router(rank_router)
router.include_router(jurisdiction_router)

router.include_router(router_education)
router.include_router(anthropometric_data_router)
router.include_router(dispensary_registrations_router)
router.include_router(age_group_router)
router.include_router(general_user_information_router)
router.include_router(hospital_data_router)
router.include_router(medical_profile_router)
router.include_router(user_liberation_router)
router.include_router(profile_router)
router.include_router(personal_profile_router)
router.include_router(family_status_router)
router.include_router(biographic_info_router)
router.include_router(driving_license_router)
router.include_router(identification_card_router)
router.include_router(passport_router)
router.include_router(sport_achievement_router)
router.include_router(sport_degree_router)
router.include_router(tax_declaration_router)
router.include_router(user_financial_info_router)
router.include_router(abroad_travel_router)
router.include_router(additional_profile_router)
router.include_router(polygraph_check_router)
router.include_router(psychological_check_router)
router.include_router(special_check_router)
router.include_router(violation_router)
router.include_router(properties_router)
router.include_router(property_type_router)
router.include_router(family_router)
router.include_router(service_housing_router)
router.include_router(vehicle_router)

router.include_router(staff_list_router)
router.include_router(country_router)
