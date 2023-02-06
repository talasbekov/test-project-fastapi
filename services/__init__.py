# Be careful of imports order is important!
# Possible problems are circular imports, partial initialization of module

from .hr_document import hr_document_service
# Keep in mind that I have hr_document_service in this file
# So I need to make sure that it will initialize before initializing my file
from .hr_document_template import hr_document_template_service
