from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .user import User # импорт User произойдёт только для анализаторов типов, в рантайме — нет


class Post(UserRelationMixin, Base):
    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text, default="", server_default="") # для модели и внутри БД. Лучше вместе
