from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from base.database import Base
from consumers_basic.user_services.models import Mixin


class User(Mixin, Base):
    email: Mapped[str] = mapped_column(
        String(50), unique=True
    )
    username: Mapped[str] = mapped_column(
        String(30), unique=True
    )
    first_name: Mapped[str] = mapped_column(
        String(30)
    )
    last_name: Mapped[str] = mapped_column(
        String(30)
    )
