import os
from fastapi import Request, Form, Depends, APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from src.core.constants import BASE_DIR
from src.database.session import get_db
from src.exceptions.product_exceptions import ProductNotFoundError
from src.services.product_service import ProductService

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'templates'))

@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post('/barcode')
async def receive_barcode(barcode: str = Form(...), db: AsyncSession = Depends(get_db)):
    logger.info(f"получен код: {barcode}")
    service = ProductService(db)
    try:
        product = await service.upsert_by_code(barcode)
    except ProductNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return {
        'status': 'success',
        'sid': product.sid,
        'name': product.name,
        'price': product.price,
        'photo': product.photo_link
    }