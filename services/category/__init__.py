from .base import BaseCategory


categories = {}

# Iterate over the module variables
for name in dir():
    value = globals().get(name)
    if hasattr(value, '__handler__'):
        # Add the handler to the handlers dictionary using the __handler__ property as the key
        categories[value.__handler__] = value
