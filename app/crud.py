from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import selectinload
from app.database.db_models import SubstanceCategoryORM, SubstancesORM, Substances_SynthesesORM
from fastapi import HTTPException, status
from sqlalchemy.future import select




async def add_substance_category(session: AsyncSession, name: str, description: str)->SubstanceCategoryORM:
    new_category = SubstanceCategoryORM(
        category_name=name,
        description=description
    )
    session.add(new_category)
    try:
        await session.commit()
        await session.refresh(new_category)
        print("new_substance.id:", new_category.id)

        return new_category
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists."
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
async def get_substance_category(session: AsyncSession):
    try:
        query = select(SubstanceCategoryORM)
        result = await session.execute(query)
        categories = result.scalars().all()
        return categories
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

async def add_substance(session: AsyncSession, name: str, weight: float, category_id: int):
    try:
        result = await session.execute(
            select(SubstanceCategoryORM).where(SubstanceCategoryORM.id == category_id)
        )
        substance_category = result.scalars().first()
        if not substance_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Substance category not found"
            )

        new_substance = SubstancesORM(
            name=name,
            weight=weight,
            category_id=category_id
        )
        session.add(new_substance)
        await session.commit()
        await session.refresh(new_substance)
        return new_substance

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
async def get_substance(session: AsyncSession):
    try:
        query = select(SubstancesORM)
        result = await session.execute(query)
        substances = result.scalars().all()
        return substances
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )



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