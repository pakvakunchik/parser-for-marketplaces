import os
from typing import Optional
from fastapi import Request, Form, Depends, APIRouter, HTTPException, Query
from fastapi.templating import Jinja2Templates
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from src.core.constants import BASE_DIR
from src.database.session import get_db
from src.exceptions.product_exceptions import ProductNotFoundError
from src.integrations.github_ai import AiGenerator
from src.repositories.product_repository import ProductRepository
from src.schemas.schemas import ProductResponse, AIGenerateResponse, ProductSchema, BarcodeParserResponse, AIInputData
from src.services.product_service import ProductService
from src.services.rawdata_cleaner_service import RawDataCleaner
from src.core.constants import first_keys

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'templates'))

@router.get("/", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@router.post('/barcode', response_model=BarcodeParserResponse, status_code=status.HTTP_201_CREATED)
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

@router.post('/ai_generate', response_model=AIGenerateResponse, status_code=status.HTTP_201_CREATED)
async def generate_product_ai_content(
        product_id: Optional[int] = Query(None, description='Внутренний ID товара в БД'),
        sid: Optional[int] = Query(None, description='Артикул товара (sid) от поставщика'),
        last_added: bool = Query(False, description='Взять самый последний добавленный товар'),
        db: AsyncSession = Depends(get_db)
):
    repo = ProductRepository(db)
    product = None
    if last_added:
        product = await repo.get_last_added()
    elif product_id is not None:
        product = await repo.get_by_id(product_id)
    elif sid is not None:
        product = await repo.get_by_sid(sid)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Товар не найден. Проверьте переданные параметры'
        )
    cleaner = RawDataCleaner(raw_api_data=product.raw_api_data)
    cleaned_dict = await cleaner.clean_data(keywords=first_keys)
    clean_data_before = AIInputData.model_validate(cleaned_dict, from_attributes=True)
    ai_result = await AiGenerator.generate_name_and_description(clean_data=clean_data_before)
    update_product = await repo.update_ai_data(
        product=product,
        name_ai=ai_result.get('name'),
        description_ai=ai_result.get('description')
    )
    await db.commit()
    await db.refresh(update_product)
    data_after = ProductSchema.model_validate(update_product, from_attributes=True)
    return AIGenerateResponse(
        before=clean_data_before,
        after=data_after
    )
