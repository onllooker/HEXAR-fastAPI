import uvicorn

from app.api.api import app

if __name__ == "__main__":
    uvicorn.run(app)
