from typing import Type, TypeVar

from sqlalchemy import and_, func

from core import Base

ModelType = TypeVar("ModelType", bound=Base)

def add_filter_to_query(query, filter, model: Type[ModelType]):
    key_words = filter.lower().split()
    new_query = (
        query
        .filter(
            and_(func.concat(func.concat(func.lower(model.name), ' '),
                             func.concat(func.lower(model.nameKZ), ' '))
                 .contains(name) for name in key_words)
        )
    )
    return new_query