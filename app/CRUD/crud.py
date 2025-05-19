from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import selectinload
from app.database.db_models import SubstanceCategoryORM, SubstancesORM, Substances_SynthesesORM
from fastapi import HTTPException, status
from sqlalchemy.future import select







async def get_list_recipes(session: AsyncSession):
    result = await session.execute(
        select(Substances_SynthesesORM)
        .options(
            selectinload(Substances_SynthesesORM.syntheses),
            selectinload(Substances_SynthesesORM.substance)
        )
    )
    return result.scalars().all()

async def get_recipes_by_synthesis(session: AsyncSession, synthesis_id: int):
    result = await session.execute(
        select(Substances_SynthesesORM)
        .where(Substances_SynthesesORM.synthesis_id == synthesis_id)
        .options(
            selectinload(Substances_SynthesesORM.syntheses),
            selectinload(Substances_SynthesesORM.substance)
        )
    )
    records = result.scalars().all()
    return records

async def get_recipes_by_substance(session: AsyncSession, substance_id: int):
    result = await session.execute(
        select(Substances_SynthesesORM)
        .where(Substances_SynthesesORM.substance_id == substance_id)
        .options(
            selectinload(Substances_SynthesesORM.syntheses),
            selectinload(Substances_SynthesesORM.substance)
        )
    )
    records = result.scalars().all()