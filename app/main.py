from fastapi import FastAPI, Query, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import Annotated
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title='Reactor Monitoring System')

# class Users(BaseModel):
#     name:str
#     age:int
#     emil:str
#
# @app.get(path='/', summary='Домашняя', tags=['Основные ручки'])
# def home( qtmp: Annotated[str | None, Query(max_length=30)]=None):
#     return {"message_input"}

# Пример данных в памяти
syntheses_db = [{'id':1,
                 'name':'test',
                 'start_time':'start',
                 'end_time':'end',
                 'status':'test_time',
                 'temperature':29}]  # Список для хранения данных синтезов
alarms_db = []  # Список для хранения данных аварий

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
        return syntheses_db
    except Exception as e:
        logger.error(f"Error fetching syntheses: {e}")
        raise HTTPException(status_code=500, detail="Error fetching syntheses")

# Создание нового синтеза
@app.post("/syntheses/", response_model=SynthesisCreate)
def create_synthesis(synthesis: SynthesisCreate):
    try:
        syntheses_db.append(synthesis)
        logger.info(f"Synthesis {synthesis.id} created successfully")
        return synthesis
    except Exception as e:
        logger.error(f"Error creating synthesis: {e}")
        raise HTTPException(status_code=500, detail="Error creating synthesis")

# Получение всех аварий
@app.get("/alarms/", response_model=list[AlarmCreate])
def get_alarms():
    try:
        return alarms_db
    except Exception as e:
        logger.error(f"Error fetching alarms: {e}")
        raise HTTPException(status_code=500, detail="Error fetching alarms")

# Создание новой аварии
@app.post("/alarms/", response_model=AlarmCreate)
def create_alarm(alarm: AlarmCreate):
    try:
        alarms_db.append(alarm)
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
        alarms = [alarm for alarm in alarms_db if severity_level in alarm.message]
        return alarms
    except Exception as e:
        logger.error(f"Error fetching alarms: {e}")
        raise HTTPException(status_code=500, detail="Error fetching alarms")

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
