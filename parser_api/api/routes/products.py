from fastapi import APIRouter, HTTPException
from typing import List
from parser_api.api.schemas.schemas import ProductResponse
from parser_api.parsers.lenta_parser import AsyncLentaProductParse
import asyncio
from functools import partial

router = APIRouter()

@router.get("/products", response_model=List[ProductResponse])
async def get_products():
    """Get all products"""
    # Здесь будет логика получения продуктов из БД
    return []  # Возвращаем пустой список вместо None

@router.post("/update")
async def update_products(address: str):
    """Update products data"""
    parser = AsyncLentaProductParse(address)
    try:
        # Запускаем парсер в отдельном потоке, чтобы не блокировать event loop
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, partial(asyncio.run, parser.parse()))
        if not result:
            raise HTTPException(status_code=500, detail="Failed to parse products")
        return {"message": f"Successfully parsed {len(result)} products"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 