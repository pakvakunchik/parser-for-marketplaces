import uvicorn
from fastapi import FastAPI
from src.routers.routers import router as routers
"""
сервер стартует через:
poetry run uvicorn src.main:app --reload
"""
app = FastAPI()
app.include_router(routers)


