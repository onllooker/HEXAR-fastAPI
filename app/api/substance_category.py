from fastapi import APIRouter
from app.database.db_config import SessionDep

from app.CRUD.substances_categories_crud import add_substance_category, get_substance_category, delete_substance_category
from app.schemas.substances_category_schema import SubstanceCategoryCreateSchema, SubstanceCategoryReadSchema

substances_category_router = APIRouter(prefix="/substances_category", tags=["Substances Category"])

@substances_category_router.post("/", response_model=SubstanceCategoryReadSchema)
async def api_add_substances_category(schema:SubstanceCategoryCreateSchema, session:SessionDep):
    return await add_substance_category(session=session, schema=schema)

@substances_category_router.get("/", response_model=list[SubstanceCategoryReadSchema])
async def api_get_substances_category(session:SessionDep):
    return await get_substance_category(session=session)

@substances_category_router.delete("/{substance_category_id}", status_code=204)
async def api_delete_substance_category(substance_category_id:int, session:SessionDep):
    return await delete_substance_category(session=session, category_id=substance_category_id)