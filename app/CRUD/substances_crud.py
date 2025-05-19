from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from app.database.db_models import SubstanceCategoryORM, SubstancesORM
from app.schemas.substances_schema import SubstanceCreateSchema, SubstanceReadSchema
from fastapi import HTTPException, status

async def add_substance(session: AsyncSession, schema: SubstanceCreateSchema)->SubstanceReadSchema:
    try:
        substance_category = await session.execute(session.execute(select(SubstanceCategoryORM).filter_by(id=schema.category_id))).scalars().first()
        if not substance_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Substance category not found"
            )

        new_substance = SubstancesORM(
            name=schema.name,
            weight=schema.weight,
            description=schema.description,
            category_id=schema.category_id
        )
        session.add(new_substance)
        await session.commit()
        await session.refresh(new_substance)
        return SubstanceReadSchema.from_orm(new_substance)

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

async def get_substances(session: AsyncSession, schema: SubstanceReadSchema)->List[SubstanceReadSchema]:
    try:
        query = select(SubstancesORM)
        result = await session.execute(query)
        substances = result.scalars().all()
        return [SubstanceReadSchema.from_orm(substance) for substance in substances]
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
