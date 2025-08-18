from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base (DeclarativeBase):
    __abstract__ = True    # Без создания в базе данных

    # директивы настраивают поведение ORM, а не описывают данные.
    @declared_attr.directive    # каждый дочерний класс должен вычислить это свойство заново
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)

