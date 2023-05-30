# Imports
from .base import BaseHandler
from .add_badge import handler as add_badge_handler
from .add_black_beret import handler as add_black_beret_handler
from .add_coolness import handler as add_coolness_handler
from .add_penalty import handler as add_penalty_handler
from .add_secondment import handler as add_secondment_handler

from .decrease_coolness import handler as decrease_coolness_handler
from .decrease_rank import handler as decrease_rank_handler

from .delete_badge import handler as delete_badge_handler
from .delete_black_beret import handler as delete_black_beret_handler
from .delete_penalty import handler as delete_penalty_handler
from .delete_coolness import handler as delete_coolness_handler

from .increase_rank import handler as increase_rank_handler

from .renew_contract import handler as renew_contract_handler

from .stop_status import handler as stop_status_handler
from .temporary_status_change import handler as temporary_status_change_handler
from .status_change import handler as status_change_handler
from .position_change import handler as position_change_handler
from .confirm_coolness import handler as confirm_coolness_handler
from .apply_staff_list import handler as apply_staff_list_handler
from .superdoc import handler as superdoc_handler
from .apply_archive_position import handler as apply_archive_position_handler
from .grant_leave import handler as grant_leave_handler
from .sick_leave import handler as sick_leave_handler
from .stop_leave import handler as stop_leave_handler


# Create an empty dictionary to store the handlers
handlers = {}

# Iterate over the module variables
for name in dir():
    value = globals().get(name)
    if hasattr(value, '__handler__'):
        # Add the handler to the handlers dictionary using the __handler__ property as the key
        handlers[value.__handler__] = value
