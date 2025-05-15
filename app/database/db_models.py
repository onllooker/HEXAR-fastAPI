from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


class SensorDataORM(Base):
    __tablename__ = "sensordata"

class SubstanceCategoryORM(Base):
    __tablename__ = "substance_category"

    category_name: Mapped[str]
    description: Mapped[str | None]
    # Обратная связь: категория содержит множество веществ
    substances: Mapped[list["SubstancesORM"]] = relationship(back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SubstanceCategory(id={self.id}, category_name='{self.category_name}')>"

class Substances_SynthesesORM(Base):
    __tablename__ = "synthesis_recipe"

    synthesis_id: Mapped[int] = mapped_column(ForeignKey("syntheses.id"), primary_key=True)
    substance_id: Mapped[int] = mapped_column(ForeignKey("substances.id"), primary_key=True)
    percentage: Mapped[int]

    syntheses: Mapped["SynthesesORM"] = relationship(back_populates='substance_associations')
    substance: Mapped["SubstancesORM"] = relationship(back_populates='syntheses_associations')

class SynthesesORM(Base):
    __tablename__ = "syntheses"

    name:Mapped[str] = mapped_column(unique=True)
    description:Mapped[str]

    substances: Mapped[list["SubstancesORM"]] = relationship(secondary="synthesis_recipe", back_populates="synthesis")
    substance_associations: Mapped[list["Substances_SynthesesORM"]] = relationship(back_populates="syntheses")

    @property
    def recipe(self):
        return self.substance_associations


class SubstancesORM(Base):
    __tablename__ = "substances"

    name: Mapped[str] = mapped_column(unique=True)
    weight: Mapped[float]
    description: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("substance_category.id"))

    category: Mapped["SubstanceCategoryORM"] = relationship(back_populates="substances")
    synthesis: Mapped[list["SynthesesORM"]] = relationship(secondary="synthesis_recipe", back_populates='substances')
    syntheses_associations: Mapped[list["Substances_SynthesesORM"]] =relationship(back_populates="substance")
