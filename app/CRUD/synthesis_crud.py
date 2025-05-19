from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_models import Substances_SynthesesORM, SubstancesORM, SynthesesORM
from app.schemas.synthesis_schema import (
    RecipeCreateSchema,
    SynthesisCreateSchema,
    SynthesisReadSchema,
)


async def add_synthesis(session: AsyncSession, schema: SynthesisCreateSchema) -> SynthesisReadSchema:
    new_syn = SynthesesORM(
        name=schema.name,
        description=schema.description,
    )
    session.add(new_syn)
    await session.flush()

    for recipe_item in schema.recipe:
        assoc = Substances_SynthesesORM(
            synthesis_id=new_syn.id,
            substance_id=recipe_item.substance_id,
            percentage=recipe_item.percent,
        )
        session.add(assoc)

    await session.commit()
    await session.refresh(new_syn)

    return SynthesisReadSchema.model_validate(new_syn)


async def get_syntheses(session: AsyncSession) -> list[SynthesisReadSchema]:
    try:
        query = select(SubstancesORM)
        result = await session.execute(query)
        syntheses = result.scalars().all()
        return [SynthesisReadSchema.model_validate(synthesis) for synthesis in syntheses]
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")


async def update_synthesis(session: AsyncSession, synthesis_id: int, schema: RecipeCreateSchema) -> SynthesisReadSchema:
    raise NotImplementedError()


async def delete_substance_from_synthesis(session: AsyncSession, synthesis_id: int) -> None:
    raise NotImplementedError()
