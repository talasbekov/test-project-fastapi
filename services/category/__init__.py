from .base import BaseCategory

from .curators import handler as curators_handler
from .pgs import handler as pgs_handler
from .supervisors import handler as supervisors_handler

categories = {}

# Iterate over the module variables
for name in dir():
    value = globals().get(name)
    if hasattr(value, "__handler__"):
        # Add the handler to the handlers dictionary using the __handler__
        # property as the key
        categories[value.__handler__] = value
