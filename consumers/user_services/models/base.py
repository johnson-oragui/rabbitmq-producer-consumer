from sqlalchemy.orm import (
    declarative_mixin,
    declared_attr,
    Mapped,
    mapped_column
)
from sqlalchemy import String, DateTime, func
from uuid import uuid4
from datetime import datetime

def get_id():
    """
    gets uuid as str
    """
    return str(uuid4())

@declarative_mixin
class Mixin:
    """
    Base class for model mixin
    """
    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True,
        default=get_id
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
        onupdate=func.now()
    )

    @declared_attr
    @classmethod
    def __tablename__(cls):
        """
        table names
        """
        return f'{cls.__name__.lower()}s'
