import os
from fastapi import Request, Form, Depends, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse
from src.core.constants import BASE_DIR
from src.integrations.supplier_api import get_item_from_supplier
from src.database.models import Product
from src.database.session import get_db
from src.services.photo_service import get_photo

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
    raw_data = await get_item_from_supplier(barcode)
    if not raw_data:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'status': 'error',
                'message': 'Товар не найден'
                     }
        )
    sid = raw_data.get('sid')
    stmt = select(Product).where(Product.sid == sid)
    result = await db.execute(stmt)
    existing_product = result.scalars().first()
    if existing_product:
        existing_product.quantity += 1
        await db.commit()
        await db.refresh(existing_product)
        product = existing_product
        logger.info(f'Товар {product.sid, product.name} обновлён')
    else:
        product = Product(
            sid=sid,
            name=raw_data.get('name', '')[:50],
            price=float(raw_data.get('price', 0)),
            wholesale_price=float(raw_data.get('wholesale_price')),
            barcode=barcode,
            raw_api_data=raw_data,
            quantity_supplier=raw_data.get('balance', 0),
            quantity= + 1,
            photo_link = raw_data.get('photoUrl', None)
        )
        db.add(product)
        await db.commit()
        await db.refresh(product)
    await get_photo(raw_data)
    return {
        'status': 'success',
        'sid': sid,
        'name': raw_data.get('name'),
        'price': raw_data.get('price'),
        'photo': raw_data.get('photoUrl'),
            }