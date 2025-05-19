import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.db_config import async_engine
from app.database.db_models import Base

from .alarm import alarm_router
from .substance_category import substances_category_router
from .substnces import substances_router
from .syntheses import syntheses_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield


app = FastAPI(title="Reactor Monitoring System", lifespan=lifespan)
app.include_router(substances_category_router)
app.include_router(substances_router)
app.include_router(syntheses_router)
app.include_router(alarm_router)

#
# @app.post("/add_substance_category", summary="Add new category", tags=["Categories rout"], response_model=SubstanceCategoryScheme)
# async def api_add_substance_category(scheme: SubstanceCategoryCreateScheme, session: SessionDep):
#     return await add_substance_category(session, scheme.category_name, scheme.description)
#
#
# @app.get("/get_substance_category", summary="Get all categories", tags=["Categories rout"], response_model=SubstanceCategoryScheme)
# async def api_get_substance_category(session: SessionDep):
#     return await get_substance_category(session = session)
#
#
# @app.post("/add_substance", summary='Add substances description', tags=['Substances routs'], response_model=SubstanceScheme)
# async def api_add_substance(substance: SubstanceCreateScheme, session: SessionDep):
#    return await add_substance(session, name=substance.name, weight=substance.weight, category_id=substance.category_id)
#
# @app.get("/get_substance/", summary='Get substances description', tags=['Substances routs'])
# async def api_get_substance(session: SessionDep):
#     return await get_substance(session = session)
#
# @app.post("/syntheses/")
# def create_synthesis(synthesis: SynthesesCreateScheme) -> SynthesesCreateScheme:
#     try:
#
#         logger.info(f"Synthesis {synthesis.id} created successfully")
#         return {"message":"Success"}
#     except Exception as e:
#         logger.error(f"Error creating synthesis: {e}")
#         raise HTTPException(status_code=500, detail="Error creating synthesis")
#
#
# @app.get("/syntheses/", response_model=list[SynthesesCreateScheme])
# def get_syntheses():
#     try:
#         return ...
#     except Exception as e:
#         logger.error(f"Error fetching syntheses: {e}")
#         raise HTTPException(status_code=500, detail="Error fetching syntheses")
#
#
#
#
# # Получение всех аварий
# @app.get("/alarms/", response_model=list[AlarmScheme])
# def get_alarms():
#     try:
#         return ...
#     except Exception as e:
#         logger.error(f"Error fetching alarms: {e}")
#         raise HTTPException(status_code=500, detail="Error fetching alarms")
#
#
# # Создание новой аварии
# @app.post("/alarms/", response_model=AlarmScheme)
# def create_alarm(alarm: AlarmScheme):
#     try:
#         logger.info(f"Alarm {alarm.id} created successfully")
#         return alarm
#     except Exception as e:
#         logger.error(f"Error creating alarm: {e}")
#         raise HTTPException(status_code=500, detail="Error creating alarm")
#
#
# # Команды для управления синтезом
# @app.post("/control/start/")
# def start_synthesis():
#     try:
#         logger.info("Starting synthesis process...")
#         return {"message": "Synthesis started successfully"}
#     except Exception as e:
#         logger.error(f"Error starting synthesis: {e}")
#         raise HTTPException(status_code=500, detail="Error starting synthesis")
#
#
# @app.post("/control/stop/")
# def stop_synthesis():
#     try:
#         logger.info("Stopping synthesis process...")
#         return {"message": "Synthesis stopped successfully"}
#     except Exception as e:
#         logger.error(f"Error stopping synthesis: {e}")
#         raise HTTPException(status_code=500, detail="Error stopping synthesis")
#
#
# # Эндпоинты для получения текущих параметров
# @app.get("/status/")
# def get_current_status():
#     try:
#         # Пример статуса синтеза
#         return {"status": "Running", "temperature": 75}
#     except Exception as e:
#         logger.error(f"Error fetching current status: {e}")
#         raise HTTPException(status_code=500, detail="Error fetching current status")
#
#
# # Эндпоинт для получения аварий по критериям
# @app.get("/alarms/{severity_level}", response_model=list[AlarmCreateScheme])
# def get_alarms_by_severity(severity_level: str):
#     try:
#         # Пример фильтрации по критичности
#         return ...
#     except Exception as e:
#         logger.error(f"Error fetching alarms: {e}")
#         raise HTTPException(status_code=500, detail="Error fetching alarms")
#
#
# @app.post("/make_new_synthesis")
# async def make_new_synthesis():
#     return {"message": "i am alive"}
#
#
# @app.get("/list_recipes", summary="Get all recipes", tags=["Recipes routs"])
# async def api_get_list_recipes(session: SessionDep):
#     return await get_list_recipes(session=session)
#
# @app.get("/by-synthesis/{synthesis_id}", summary="Get recipes by synthesis_id", tags=["Recipes routs"])
# async def api_get_recipes_by_synthesis(session: SessionDep):
#     return await get_recipes_by_synthesis(session=session)
#
# @app.get("/by-substance/{substance_id}", summary="Get recipes by substance_id", tags=["Recipes routs"])
# async def api_get_recipes_by_substance(session: SessionDep):
#     return await get_recipes_by_substance(session=session)
