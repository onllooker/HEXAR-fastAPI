from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import ForeignKey
from typing import Annotated


class Base(DeclarativeBase):
    __abstract__ = True
    id:Mapped[int] = mapped_column(primary_key=True)


class SynthesesORM(Base):
    __tablename__ = "syntheses"

    name:Mapped[str] = mapped_column(unique=True)
    discription:Mapped[str]

class SensorDataORM(Base):
    __tablename__ = "sensordata"

class SubstancesORM(Base):
    __tablename__ = "substances"

    name: Mapped[str] = mapped_column(unique=True)
    weight: Mapped[float]
    category_id: Mapped[str] = mapped_column(ForeignKey("substance_category.id"))

    category: Mapped["SubstanceCategoryORM"] = relationship(back_populates="substances")


class SubstanceCategoryORM(Base):
    __tablename__ = 'substance_category'

    category_name: Mapped[str]
    description: Mapped[str | None]
    # Обратная связь: категория содержит множество веществ
    substances: Mapped[list["SubstancesORM"]] = relationship(back_populates="category", cascade="all, delete-orphan"
)

    def __repr__(self):
        return f"<SubstanceCategory(id={self.id}, category_name='{self.category_name}')>"


# class Substunces_SynthesesORM(Base):
#     __tablename__ = 'synthesis_recipe'
#
#     synthesis_id: Mapped[int] = mapped_column(ForeignKey('syntheses.id'), nullable=False)
#     substance_id: Mapped[int] = mapped_column(ForeignKey('substance.id'), nullable=False)
#     percentage: Mapped[int]
#     # Определяем отношения для доступа к синтезу и веществу
#     synthesis = relationship('SynthesesORM', back_populates='synthesis_recipes')
#     substance = relationship('SubstancesORM', back_populates='synthesis_recipes')
