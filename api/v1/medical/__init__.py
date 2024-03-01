from fastapi import APIRouter

from .anthropometric_data import router as anthropometric_data_router
from .dispensary_registrations import router as dispensary_registrations_router
from .age_group import router as age_group_router
from .blood_type import router as blood_type_router
from .general_user_information import router as general_user_information_router
from .hospital_data import router as hospital_data_router
from .medical_profile import router as medical_profile_router
from .user_liberation import router as user_liberation_router
from .liberation import router as liberation_router


router_medical= APIRouter(prefix="/medical")

router_medical.include_router(anthropometric_data_router)
router_medical.include_router(dispensary_registrations_router)
router_medical.include_router(age_group_router)
router_medical.include_router(general_user_information_router)
router_medical.include_router(hospital_data_router)
router_medical.include_router(medical_profile_router)
router_medical.include_router(user_liberation_router)
router_medical.include_router(liberation_router)
router_medical.include_router(blood_type_router)
