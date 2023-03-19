import uuid

from sqlalchemy import TIMESTAMP, Column, String, text
from sqlalchemy.dialects.postgresql import UUID

from core import Base

"""
    This class is abstract entity class, which provides following columns to all inherited entities:
    - **id** : UUID - clustered index of table
    - **created_at**: datetime - Creation timestamp of entity
    - **updated_at**: datetime - Update timestamp of entity
"""


class Model(Base):

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


"""
    This class is abstract entity class, which provides following columns to all inherited entities:
    - **name** : str - required
"""


class NamedModel(Model):

    __abstract__ = True

    name = Column(String, nullable=False)


"""
    This class is abstract entity class, which can be nested. This is merely markdown of nested classes. This Model doesn't do anything except marking all nested classes
"""


class NestedModel(Model):

    __abstract__ = True


"""
    This class is abstract entity class, which can be nested. This is merely markdown of nested classes. This Model doesn't do anything except marking all nested classes.
    Only difference between nested models is **name**
"""


class NamedNestedModel(NamedModel):

    __abstract__ = True
