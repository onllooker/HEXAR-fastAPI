from fastapi import APIRouter
from app.database.db_config import SessionDep
from app.CRUD.substances_crud import add_substance, get_substances

substances_router = APIRouter(prefix="/substances")

@substances_router.post("/")
async def api_add_substance(session: SessionDep):
    return await add_substance(session=session)

@substances_router.get("/")
async def api_get_substances(session: SessionDep):
    return await get_substances(session=session)