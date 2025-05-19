from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_models import SubstanceCategoryORM
from app.schemas.substances_category_schema import (
    SubstanceCategoryCreateSchema,
    SubstanceCategoryReadSchema,
)

from .utils import get_by_id


async def add_substance_category(session: AsyncSession, schema: SubstanceCategoryCreateSchema) -> SubstanceCategoryReadSchema:
    new_category = SubstanceCategoryORM(category_name=schema.category_name, description=schema.description)
    try:
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        return SubstanceCategoryReadSchema.model_validate(new_category)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(400, "Category with this name already exists.")
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(500, "Internal database error.")


async def get_substance_category(session: AsyncSession) -> List[SubstanceCategoryReadSchema]:
    try:
        query = select(SubstanceCategoryORM)
        result = await session.execute(query)
        categories = result.scalars().all()
        return [SubstanceCategoryReadSchema.model_validate(category) for category in categories]
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")


async def delete_substance_category(session: AsyncSession, category_id: int):
    category = await get_by_id(session, SubstanceCategoryORM, category_id)
    try:
        await session.delete(category)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
