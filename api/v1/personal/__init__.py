from fastapi import APIRouter

from .family_status import router as family_status_router
from .biographic_info import router as biographic_info_router
from .driving_license import router as driving_license_router
from .identification_card import router as identification_card_router
from .passport import router as passport_router
from .personal_profile import router as personal_profile_router
from .sport_achievement import router as sport_achievement_router
from .sport_degree import router as sport_degree_router
from .tax_declaration import router as tax_declaration_router
from .user_financial_info import router as user_financial_info_router
from .sport_type import router as sport_type_router
from .sport_degree_type import router as sport_degree_type_router
from .citizenship import router as citizenship_router
from .nationality import router as nationality_router
from .birthplace import router as birthplace_router
from .city import router as city_router
from .region import router as region_router

personal_router = APIRouter(prefix="/personal")

personal_router.include_router(family_status_router)
personal_router.include_router(biographic_info_router)
personal_router.include_router(driving_license_router)
personal_router.include_router(identification_card_router)
personal_router.include_router(passport_router)
personal_router.include_router(personal_profile_router)
personal_router.include_router(sport_achievement_router)
personal_router.include_router(sport_degree_router)
personal_router.include_router(tax_declaration_router)
personal_router.include_router(user_financial_info_router)
personal_router.include_router(sport_type_router)
personal_router.include_router(sport_degree_type_router)
personal_router.include_router(citizenship_router)
personal_router.include_router(nationality_router)
personal_router.include_router(birthplace_router)
personal_router.include_router(city_router)
personal_router.include_router(region_router)
