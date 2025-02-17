from .base import BaseAutoTagHandler

from .registration_address import handler as registration_address_handler
from .birthday import handler as birthday_handler
from .total_day import handler as total_day_handler
from .service_day import handler as service_day_handler
from .work_day import handler as work_day_handler
from .total_month import handler as total_month_handler
from .service_month import handler as service_month_handler
from .work_month import handler as work_month_handler
from .total_year import handler as total_year_handler
from .service_year import handler as service_year_handler
from .work_year import handler as work_year_handler
from .position import handler as position_handler
from .surname import handler as surname_handler
from .name import handler as name_handler
from .father_name import handler as father_name_handler
from .rank import handler as rank_handler
from .family_member import handler as family_members_handler
from .officer_number import handler as officer_number_handler

auto_tags = {}

for name in dir():
    value = globals().get(name)
    if hasattr(value, "__handler__"):
        # Add the handler to the handlers dictionary using the __handler__
        # property as the key
        auto_tags[value.__handler__] = value
