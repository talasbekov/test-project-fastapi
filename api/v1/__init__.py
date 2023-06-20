from fastapi import APIRouter

from .education import router_education

from .hr_document import router as hr_document_router
from .render import router as render_router
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
from .privelege_emergency import router as privelege_emergency_router
from .personnal_reserve import router as personnal_reserve_router
from .coolness import router as coolness_router
from .user_oath import router as user_oauth_router
from .military_unit import router as military_unit_router
from .recommender_user import router as recommender_user_router
from .notification import router as notification_router
from .action import router as action_router
from .hr_vacancy import router as hr_vacancy_router
from .hr_vacancy_requirement import router as hr_vacancy_requirement_router
from .position import router as position_router
from .auto_tag import router as auto_tag_router

from .survey import *

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(action_router)
router.include_router(auto_tag_router)
router.include_router(render_router)
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
router.include_router(notification_router)


router.include_router(privelege_emergency_router)
router.include_router(coolness_router)
router.include_router(personnal_reserve_router)


router.include_router(router_education)
router.include_router(router_medical)
router.include_router(profile_router)
router.include_router(personal_router)
router.include_router(additional_router)
router.include_router(family_router)

router.include_router(staff_list_router)

router.include_router(archive_staff_division_router)
router.include_router(archive_service_staff_function_type_router)
router.include_router(archive_service_staff_function_router)
router.include_router(archive_document_staff_function_router)
router.include_router(archive_staff_function_router)
router.include_router(archive_staff_unit_router)
router.include_router(candidate_router)
router.include_router(candidate_stage_info_router)
router.include_router(candidate_stage_type_router)
router.include_router(candidate_stage_question_type_router)
router.include_router(candidate_stage_question_router)
router.include_router(candidate_essay_type_router)
router.include_router(candidate_category_router)
router.include_router(candidate_stage_answer_router)
router.include_router(history_router)
router.include_router(service_id_router)
router.include_router(history_name_change_router)
router.include_router(user_oauth_router)
router.include_router(military_unit_router)
router.include_router(recommender_user_router)
router.include_router(hr_vacancy_router)
router.include_router(hr_vacancy_requirement_router)
router.include_router(position_router)

router.include_router(survey_type_router)
router.include_router(survey_router)
router.include_router(question_type_router)
router.include_router(question_router)
router.include_router(option_router)
router.include_router(answer_router)
