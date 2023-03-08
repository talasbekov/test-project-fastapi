from fastapi import APIRouter

from .profile import router as profile_router
from .academic_degree import router as academic_degree_router
from .academic_degree_degree import router as academic_degree_degree_router
from .academic_title import router as academic_title_router
from .academic_degree import router as academic_degree_router
from .education import router as education_router
from .education_profile import router as educational_profile_router
from .institution import router as institution_router
from .institution_degree_type import router as institution_degree_type_router
from .language import router as language_router
from .language_proficiency import router as language_proficiency_router
from .science import router as science_router
from .specialty import router as specialty_router
from .course import router as course_router
from .course_provider import router as course_provider_router

router_education = APIRouter(prefix="/education")

router_education.include_router(profile_router)
router_education.include_router(academic_degree_router)
router_education.include_router(academic_degree_degree_router)
router_education.include_router(academic_title_router)
router_education.include_router(academic_degree_router)
router_education.include_router(education_router)
router_education.include_router(educational_profile_router)
router_education.include_router(institution_router)
router_education.include_router(institution_degree_type_router)
router_education.include_router(language_router)
router_education.include_router(language_proficiency_router)
router_education.include_router(science_router)
router_education.include_router(specialty_router)
router_education.include_router(course_router)
router_education.include_router(course_provider_router)
