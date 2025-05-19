from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from app.database.db_models import SubstanceCategoryORM, SubstancesORM
from .utils import get_by_id
from app.schemas.substances_schema import SubstanceCreateSchema, SubstanceReadSchema
from fastapi import HTTPException, status

async def add_substance(session: AsyncSession, schema: SubstanceCreateSchema)->SubstanceReadSchema:
    await get_by_id(session, SubstanceCategoryORM, schema.category_id, not_found_detail="Substance category not found")
    try:
        new_substance = SubstancesORM(
            name=schema.name,
            weight=schema.weight,
            description=schema.description,
            category_id=schema.category_id
        )
        session.add(new_substance)
        await session.commit()
        await session.refresh(new_substance)
        return SubstanceReadSchema.model_validate(new_substance)

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Substance with this name or parameters already exists."
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

async def get_substances(session: AsyncSession)->List[SubstanceReadSchema]:
    try:
        query = select(SubstancesORM)
        result = await session.execute(query)
        substances = result.scalars().all()
        return [SubstanceReadSchema.model_validate(substance) for substance in substances]
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

async def delete_substance(session:AsyncSession, substance_id: int):
    substance = await get_by_id(session, SubstancesORM, substance_id)
    try:
        await session.delete(substance)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )