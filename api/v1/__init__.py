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
from .additional import additional_router
from .medical import router_medical
from .profile import router as profile_router
from .personal import personal_router
from .family import family_router
from .staff_list import router as staff_list_router
from .archive import *
from .user_candidates import *
from .history import *
from .service_id import router as service_id_router

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
router.include_router(router_medical)
router.include_router(profile_router)
router.include_router(personal_router)
router.include_router(additional_router)
router.include_router(family_router)

router.include_router(staff_list_router)

router.include_router(archive_staff_division_router)
router.include_router(archive_service_staff_function_type_router)
router.include_router(archive_staff_function_router)
router.include_router(archive_staff_unit_router)

router.include_router(candidate_router)
router.include_router(candidate_stage_router)
router.include_router(candidate_stage_info_router)
router.include_router(candidate_stage_question_type_router)
router.include_router(candidate_stage_question_router)
router.include_router(candidate_essay_type_router)
router.include_router(candidate_stage_type_router)
router.include_router(candidate_stage_answer_router)
router.include_router(history_router)
router.include_router(service_id_router)
router.include_router(history_name_change_router)
