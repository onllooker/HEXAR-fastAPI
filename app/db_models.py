from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import ForeignKey
from typing import Annotated


class Base(DeclarativeBase):
    __abstract__ = True
    id:Mapped[int] = mapped_column(primary_key=True)



class SensorDataORM(Base):
    __tablename__ = "sensordata"


class SubstanceCategoryORM(Base):
    __tablename__ = 'substance_category'

    category_name: Mapped[str]
    description: Mapped[str | None]
    # Обратная связь: категория содержит множество веществ
    substances: Mapped[list["SubstancesORM"]] = relationship(back_populates="category", cascade="all, delete-orphan"
)

    def __repr__(self):
        return f"<SubstanceCategory(id={self.id}, category_name='{self.category_name}')>"


class Substances_SynthesesORM(Base):
    __tablename__ = 'synthesis_recipe'

    synthesis_id: Mapped[int] = mapped_column(ForeignKey('syntheses.id'), primary_key=True)
    substance_id: Mapped[int] = mapped_column(ForeignKey('substances.id'), primary_key=True)
    percentage: Mapped[int]

    syntheses: Mapped["SynthesesORM"] = relationship(back_populates='syntheses_associations')
    substance: Mapped["SubstancesORM"] = relationship(back_populates='substance_associations')

class SynthesesORM(Base):
    __tablename__ = "syntheses"

    name:Mapped[str] = mapped_column(unique=True)
    discription:Mapped[str]

    substances: Mapped[list["SubstancesORM"]] = relationship(secondary="synthesis_recipe", back_populates="syntheses")
    substance_associations: Mapped[list["Substunces_SynthesesORM"]] = relationship(back_populates="syntheses")

class SubstancesORM(Base):
    __tablename__ = "substances"

    name: Mapped[str] = mapped_column(unique=True)
    weight: Mapped[float]
    category_id: Mapped[int] = mapped_column(ForeignKey("substance_category.id"))

    category: Mapped["SubstanceCategoryORM"] = relationship(back_populates="substances")
    synthesis = relationship(secondary="synthesis_recipe", back_populates='substances')
    syntheses_associations: Mapped[list["Substunces_SynthesesORM"]] =relationship(back_populates="substance")
