from typing import Any
from pydantic import BaseModel


class AutoTagRead(BaseModel):
    name: Any
    nameKZ: Any
