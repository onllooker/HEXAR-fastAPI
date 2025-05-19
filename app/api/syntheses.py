from typing import List
from fastapi import APIRouter
from app.database.db_models import SynthesesORM, SubstancesORM, Substances_SynthesesORM
from app.database.db_config import SessionDep
from app.schemas.substances_category_schema import *
from sqlalchemy import select
from app.CRUD.synthesis_crud import add_synthesis, get_syntheses
from app.schemas.synthesis_schema import SynthesisReadSchema, SynthesisCreateSchema

syntheses_router = APIRouter(prefix="/syntheses", tags=["Syntheses"])

@syntheses_router.post("/", response_model=SynthesisReadSchema)
async def api_add_synthesis(schema:SynthesisCreateSchema, session:SessionDep):
    return await add_synthesis(session=session, schema=schema)

@syntheses_router.get("/", response_model=List[SynthesisReadSchema])
async def api_get_syntheses(session:SessionDep):
    return await get_syntheses(session=session)

@syntheses_router.patch("/{synthesis_id}")
async def api_update_synthesis():
    pass

@syntheses_router.delete("/{synthesis_id}")
async def api_delete_substance_from_synthesis(synthesis_id:int):
    pass

# @syntheses_router.post("/", response_model=SynthesesScheme)
# async def create_synthesis(
#     payload: SynthesesCreateScheme,
#     session: SessionDep
# ):
#     # Ensure unique name
#     result = await session.execute(select(SynthesesORM).filter_by(name=payload.name))
#     if result.scalars().first():
#         raise HTTPException(status_code=409, detail="Synthesis with this name already exists")
#
#     synth = SynthesesORM(name=payload.name, description=payload.description)
#     session.add(synth)
#     await session.flush()
#
#     # Add recipe entries
#     for item in payload.recipe:
#         sub = await session.get(SubstancesORM, item.substance_id)
#         if not sub:
#             raise HTTPException(status_code=404, detail=f"Substance {item.substance_id} not found")
#         assoc = Substances_SynthesesORM(
#             synthesis_id=synth.id,
#             substance_id=item.substance_id,
#             percentage=item.percentage,
#         )
#         session.add(assoc)
#     await session.commit()
#     await session.refresh(synth)
#
#     recipe_out = [
#         {"substance": SubstanceScheme.from_orm(assoc.substance), "percentage": assoc.percentage}
#         for assoc in synth.substance_associations
#     ]
#     return SynthesisRead(
#         id=synth.id,
#         name=synth.name,
#         description=synth.description,
#         recipe=recipe_out,
#     )
# @syntheses_router.get("/", response_model=list[schemas.SynthesesScheme])
# async def list_syntheses(session: SessionDep):
#     result = await session.execute(select(SynthesesORM).options(
#         relationship(Substances_SynthesesORM)
#     ))
#     synths = result.scalars().unique().all()
#     output = []
#     for synth in synths:
#         recipe = [SubstancePercentage(
#             substance_id=a.substance_id,
#             percentage=a.percentage
#         ) for a in synth.substance_associations]
#         output.append(SynthesisRead(
#             id=synth.id,
#             name=synth.name,
#             description=synth.description,
#             recipe=recipe
#         ))
#     return output
#
# @syntheses_router.get("/{synthesis_id}", response_model=schemas.SynthesesScheme)
# async def get_synthesis(synthesis_id: int, session: SessionDep):
#     synth = await session.get(SynthesesORM, synthesis_id)
#     if not synth:
#         raise HTTPException(status_code=404, detail="Synthesis not found")
#     recipe = [SubstancePercentage(
#         substance_id=a.substance_id,
#         percentage=a.percentage)
#         for a in synth.substance_associations]
#     return SynthesisRead(
#         id=synth.id,
#         name=synth.name,
#         description=synth.description,
#         recipe=recipe
#     )
#
# @syntheses_router.patch("/{synthesis_id}", response_model=schemas.SynthesesScheme)
# async def update_synthesis(synthesis_id: int, payload: SynthesisUpdate, session: SessionDep):
#     synth = await session.get(SynthesesORM, synthesis_id)
#     if not synth:
#         raise HTTPException(status_code=404, detail="Synthesis not found")
#     if payload.name:
#         synth.name = payload.name
#     if payload.description:
#         synth.description = payload.description
#     session.add(synth)
#     await session.commit()
#     await session.refresh(synth)
#     recipe = [SubstancePercentage(substance_id=a.substance_id, percentage=a.percentage)
#               for a in synth.substance_associations]
#     return SynthesisRead(id=synth.id, name=synth.name, description=synth.description, recipe=recipe)
#
# @syntheses_router.patch("/{synthesis_id}", response_model=SynthesisRead, description="Частичное обновление синтеза: имя/описание и/или добавление новых веществ")
# async def update_synthesis(
#     synthesis_id: int,
#     payload: SynthesisPatch,
#     session: AsyncSession = Depends(get_async_session)
# ):
#     synth = await session.get(SynthesesORM, synthesis_id)
#     if not synth:
#         raise HTTPException(status_code=404, detail="Synthesis not found")
#
#     # Частичное обновление полей
#     if payload.name is not None:
#         synth.name = payload.name
#     if payload.description is not None:
#         synth.description = payload.description
#
#     # Добавление новых веществ в рецепт
#     if payload.recipe_to_add:
#         for item in payload.recipe_to_add:
#             sub = await session.get(SubstancesORM, item.substance_id)
#             if not sub:
#                 raise HTTPException(status_code=404, detail=f"Substance {item.substance_id} not found")
#             # Проверяем, нет ли уже такой связи
#             existing = await session.get(
#                 Substances_SynthesesORM,
#                 {"synthesis_id": synthesis_id, "substance_id": item.substance_id}
#             )
#             if existing:
#                 existing.percentage = item.percentage
#             else:
#                 assoc = Substances_SynthesesORM(
#                     synthesis_id=synthesis_id,
#                     substance_id=item.substance_id,
#                     percentage=item.percentage
#                 )
#                 session.add(assoc)
#
#     await session.commit()
#     await session.refresh(synth)
#
#     # Собираем ответ
#     recipe = [
#         SubstancePercentage(substance_id=a.substance_id, percentage=a.percentage)
#         for a in synth.substance_associations
#     ]
#     return Synthesis(
#         id=synth.id,
#         name=synth.name,
#         description=synth.description,
#         recipe=recipe
#     )
#
# @syntheses_router.delete("/{synthesis_id}}", status_code=204)
# async def remove_substance_from_synthesis(synthesis_id: int, substance_id: int, session: SessionDep):
#     assoc = await session.get(
#         Substances_SynthesesORM, {'synthesis_id': synthesis_id, 'substance_id': substance_id}
#     )
#     if not assoc:
#         raise HTTPException(status_code=404, detail="Association not found")
#     await session.delete(assoc)
#     await session.commit()
#     return {"Deleted success":" "}
