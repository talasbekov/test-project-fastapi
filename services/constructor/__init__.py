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


handlers = {
    "add_badge": add_badge_handler,
    "delete_badge": delete_badge_handler,
    "increase_rank": increase_rank_handler,
    "add_black_beret": add_black_beret_handler,
    "decrease_rank": decrease_rank_handler,
    "renew_contract": renew_contract_handler,
    "stop_status": stop_status_handler,
    "temporary_status_change": temporary_status_change_handler,
    "status_change": status_change_handler,
    "add_penalty": add_penalty_handler,
    "delete_penalty": delete_penalty_handler,
    "delete_black_beret": delete_black_beret_handler,
    "add_coolness": add_coolness_handler,
    "decrease_coolness": decrease_coolness_handler,
    "delete_coolness": delete_coolness_handler,
    "add_secondment": add_secondment_handler,
    "position_change": position_change_handler,
    "confirm_coolness": confirm_coolness_handler,
    "superdoc": superdoc_handler,
    "apply_staff_list": apply_staff_list_handler,
    "apply_archive_position": apply_archive_position_handler,
    'grant_leave': grant_leave_handler,
    'sick_leave': sick_leave_handler,
    'stop_leave': stop_leave_handler,
}
