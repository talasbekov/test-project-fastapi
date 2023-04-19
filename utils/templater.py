# -*- coding: utf-8 -*-

"""
DocPart

    New class (DocPart) that inherits from docx.parts.document.DocumentPart and overrides the next_id function.

    It should have a bug in docx (not docxtpl) in docx/parts/document.py in the way word object id's are computed:
    in the case one give many times the same image, they got the same id and MSWorld does not like it.

    So it is necessary set a random
"""

import random
from docx.parts.document import DocumentPart
from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.part import PartFactory


class DocPart(DocumentPart):

    @property
    def next_id(self):
        """Next available positive integer id value in this document.

        Calculated by incrementing maximum existing id value. Gaps in the
        existing id sequence are not filled. The id attribute value is unique
        in the document, without regard to the element type it appears on.
        """
        return random.randint(1000, 1_000_000_000)


PartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = DocPart
