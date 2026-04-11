from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from loguru import logger

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/barcode')
async def receive_barcode(barcode: str = Form(...)):
    logger.info(f"получен баркод: {barcode}")
    return {'status': 'success', 'barcode': barcode}