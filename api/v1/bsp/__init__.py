from fastapi import APIRouter

from .activity import router as activity_router
from .attendance import router as attendance_router
from .exam import router as exam_router
from .place import router as place_router
from .plan import router as plan_router
from .schedule_day import router as schedule_day_router
from .schedule_month import router as schedule_month_router
from .schedule_year import router as schedule_year_router
from .activity_type import router as activity_type_router

bsp_router = APIRouter()

bsp_router.include_router(activity_router)
bsp_router.include_router(attendance_router)
bsp_router.include_router(exam_router)
bsp_router.include_router(place_router)
bsp_router.include_router(plan_router)
bsp_router.include_router(schedule_day_router)
bsp_router.include_router(schedule_month_router)
bsp_router.include_router(schedule_year_router)
bsp_router.include_router(activity_type_router)
