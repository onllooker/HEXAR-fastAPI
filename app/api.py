import logging

from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from app.database import SessionDep, async_engine
from app.db_models import *
from app.schemas import *

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Reactor Monitoring System")


# Модели для FastAPI (Pydantic)
class SynthesisCreate(BaseModel):
    id: int
    name: str
    start_time: str
    end_time: str
    status: str
    temperature: int


class AlarmCreate(BaseModel):
    id: int
    message: str
    timestamp: str


# Получение всех синтезов
@app.get("/syntheses/", response_model=list[SynthesisCreate])
def get_syntheses():
    try:
        return ...
    except Exception as e:
        logger.error(f"Error fetching syntheses: {e}")
        raise HTTPException(status_code=500, detail="Error fetching syntheses")


# Создание нового синтеза
@app.post("/syntheses/")
def create_synthesis(synthesis: SynthesisCreate) -> SynthesisCreate:
    try:
        logger.info(f"Synthesis {synthesis.id} created successfully")
        return synthesis
    except Exception as e:
        logger.error(f"Error creating synthesis: {e}")
        raise HTTPException(status_code=500, detail="Error creating synthesis")


# Получение всех аварий
@app.get("/alarms/", response_model=list[AlarmCreate])
def get_alarms():
    try:
        return ...
    except Exception as e:
        logger.error(f"Error fetching alarms: {e}")
        raise HTTPException(status_code=500, detail="Error fetching alarms")


# Создание новой аварии
@app.post("/alarms/", response_model=AlarmCreate)
def create_alarm(alarm: AlarmCreate):
    try:
        logger.info(f"Alarm {alarm.id} created successfully")
        return alarm
    except Exception as e:
        logger.error(f"Error creating alarm: {e}")
        raise HTTPException(status_code=500, detail="Error creating alarm")


# Команды для управления синтезом
@app.post("/control/start/")
def start_synthesis():
    try:
        logger.info("Starting synthesis process...")
        return {"message": "Synthesis started successfully"}
    except Exception as e:
        logger.error(f"Error starting synthesis: {e}")
        raise HTTPException(status_code=500, detail="Error starting synthesis")


@app.post("/control/stop/")
def stop_synthesis():
    try:
        logger.info("Stopping synthesis process...")
        return {"message": "Synthesis stopped successfully"}
    except Exception as e:
        logger.error(f"Error stopping synthesis: {e}")
        raise HTTPException(status_code=500, detail="Error stopping synthesis")


# Эндпоинты для получения текущих параметров
@app.get("/status/")
def get_current_status():
    try:
        # Пример статуса синтеза
        return {"status": "Running", "temperature": 75}
    except Exception as e:
        logger.error(f"Error fetching current status: {e}")
        raise HTTPException(status_code=500, detail="Error fetching current status")


# Эндпоинт для получения аварий по критериям
@app.get("/alarms/{severity_level}", response_model=list[AlarmCreate])
def get_alarms_by_severity(severity_level: str):
    try:
        # Пример фильтрации по критичности
        return ...
    except Exception as e:
        logger.error(f"Error fetching alarms: {e}")
        raise HTTPException(status_code=500, detail="Error fetching alarms")


@app.on_event("startup")
async def on_startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/make_new_synthesis")
async def make_new_synthesis():
    """Make a new table for synthesis template"""
    return {"message": "i am alive"}


@app.post("/add_substance", summary="Add substances description", tags=["Substances routs"])
async def add_substance(substance: SubstanceCreateScheme, session: SessionDep):
    try:
        result = await session.execute(select(SubstanceCategoryORM).where(SubstanceCategoryORM.id == substance.category_id))
        substance_category = result.scalars().first()
        if not substance_category:
            raise HTTPException(status_code=404, detail="Class not found")
        new_substance = SubstancesORM(
            name=substance.name,
            weight=substance.weight,
            category_id=substance.category_id,
        )
        session.add(new_substance)
        await session.commit()
    except:
        return {"message": "Fail commit!"}


@app.get("/get_substance/", summary="Get substances description", tags=["Substances routs"])
async def get_substance(session: SessionDep):
    try:
        query = select(SubstancesORM)
        res = await session.execute(query)
        return res.scalars().all()
    except:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/add_substance_category", summary="Add new category", tags=["Categories rout"])
async def add_substance_category(scheme: SubstanceCategoryCreateScheme, session: SessionDep):
    try:
        new_category = SubstanceCategoryORM(category_name=scheme.category_name, description=scheme.description)
        session.add(new_category)
        await session.commit()
    except:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/get_substance_category", summary="Get all categories", tags=["Categories rout"])
async def get_substance_category(session: SessionDep):
    try:
        query = select(SubstanceCategoryORM)
        res = await session.execute(query)
        return res.scalars().all()
    except:
        raise HTTPException(status_code=500, detail="Internal server error")
