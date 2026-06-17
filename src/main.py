from fastapi import FastAPI
from src.routers.routers import router as product_routers
"""
сервер стартует через:
poetry run uvicorn src.main:app --reload
через тунца:
poetry run uvicorn src.main:app --host 127.0.0.1 --port 8080 --reload
"""
app = FastAPI(title='Marketplaces Refresher API')
app.include_router(product_routers)


