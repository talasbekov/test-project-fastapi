from fastapi import APIRouter

from .hr_document import router as hr_document_router
from .document_staff_function_type import router as document_staff_function_type_router
from .document_staff_function import router as document_staff_function_router
from .service_staff_function_type import router as service_staff_function_type_router
from .service_staff_function import router as service_staff_function_router
from .staff_division import router as staff_division_router
from .hr_document_info import router as hr_document_info_router
from .hr_document_step import router as hr_document_step_router
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
from .profile import router as profile_router
from .personal import (personal_profile_router, biographic_info_router, driving_licence_router,
                       identification_card_router, passport_router, sport_achievement_router,
                       sport_degree_router, tax_declaration_router, user_financial_info_router)

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(user_router)
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
router.include_router(profile_router)
router.include_router(personal_profile_router)
router.include_router(biographic_info_router)
router.include_router(driving_licence_router)
router.include_router(identification_card_router)
router.include_router(passport_router)
router.include_router(sport_achievement_router)
router.include_router(sport_degree_router)
router.include_router(tax_declaration_router)
router.include_router(user_financial_info_router)
router.include_router(abroad_travel_router)
