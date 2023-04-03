from fastapi import APIRouter

from .abroad_travel import router as abroad_travel_router
from .additional_profile import router as additional_profile_router
from .polygraph_check import router as polygraph_check_router
from .psychological_check import router as psychological_check_router
from .special_check import router as special_check_router
from .violation import router as violation_router
from .properties import router as properties_router
from .property_type import router as property_type_router
from .service_housing import router as service_housing_router
from .vehicle import router as vehicle_router
from .country import router as country_router

additional_router = APIRouter(prefix="/additional")

additional_router.include_router(abroad_travel_router)
additional_router.include_router(additional_profile_router)
additional_router.include_router(polygraph_check_router)
additional_router.include_router(psychological_check_router)
additional_router.include_router(special_check_router)
additional_router.include_router(violation_router)
additional_router.include_router(properties_router)
additional_router.include_router(property_type_router)
additional_router.include_router(service_housing_router)
additional_router.include_router(vehicle_router)
additional_router.include_router(country_router)
