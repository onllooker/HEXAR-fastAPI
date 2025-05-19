from typing import List
from fastapi import APIRouter
from app.database.db_config import SessionDep
from app.CRUD.substances_crud import add_substance, get_substances, delete_substance
from app.schemas.substances_schema import SubstanceReadSchema, SubstanceCreateSchema

substances_router = APIRouter(prefix="/substances", tags=["Substances"])

@substances_router.post("/", response_model=SubstanceReadSchema)
async def api_add_substance(session: SessionDep, schema: SubstanceCreateSchema):
    return await add_substance(session=session, schema=schema)

@substances_router.get("/", response_model=List[SubstanceReadSchema])
async def api_get_substances(session: SessionDep):
    return await get_substances(session=session)

@substances_router.delete("/{substance_id}")
async def api_delete_substance(session:SessionDep, substance_id: int):
    return await delete_substance(session=session, substance_id=substance_id)