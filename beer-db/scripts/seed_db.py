import sys
import os
from pathlib import Path
from datetime import datetime

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.services.store_service import StoreService
from app.services.product_service import ProductService
from app.models.product import (
    ProductType,
    FilteringType,
    PasteurizationType,
    SweetnessType,
    PackagingType,
    ClarificationType
)

def seed_db():
    """Seed database with test data"""
    db = SessionLocal()
    try:
        # Создаем тестовые магазины
        store_service = StoreService(db)
        stores = [
            store_service.create_store(
                address="Москва, Чонгарский бул., 7",
                city="Москва"
            )
        ]

        # Создаем тестовые товары
        product_service = ProductService(db)
        products = [
            {
                "name": "Балтика 7",
                "type": ProductType.BEER,
                "color": "Светлое",
                "is_alcoholic": True,
                "filtering": FilteringType.FILTERED,
                "pasteurization": PasteurizationType.PASTEURIZED,
                "alcohol_percentage": 4.5,
                "sweetness": SweetnessType.DRY,
                "packaging": PackagingType.GLASS_BOTTLE,
                "clarification": ClarificationType.CLEAR,
                "volume": "0.5 л",
                "price": "89.0 ₽",
                "image_url": "https://example.com/baltica7.jpg"
            },
            {
                "name": "Жигулевское",
                "type": ProductType.BEER,
                "color": "Светлое",
                "is_alcoholic": True,
                "filtering": FilteringType.FILTERED,
                "pasteurization": PasteurizationType.PASTEURIZED,
                "alcohol_percentage": 4.0,
                "sweetness": SweetnessType.DRY,
                "packaging": PackagingType.GLASS_BOTTLE,
                "clarification": ClarificationType.CLEAR,
                "volume": "0.5 л",
                "price": "79.0 ₽",
                "image_url": "https://example.com/zhigulevskoe.jpg"
            },
            {
                "name": "Клинское Темное",
                "type": ProductType.BEER,
                "color": "Темное",
                "is_alcoholic": True,
                "filtering": FilteringType.FILTERED,
                "pasteurization": PasteurizationType.PASTEURIZED,
                "alcohol_percentage": 4.8,
                "sweetness": SweetnessType.DRY,
                "packaging": PackagingType.GLASS_BOTTLE,
                "clarification": ClarificationType.CLEAR,
                "volume": "0.5 л",
                "price": "99.0 ₽",
                "image_url": "https://example.com/klinskoe_dark.jpg"
            }
        ]

        # Добавляем товары в магазины
        for store in stores:
            product_service.update_store_products(store.id, products)

        print("Database seeded successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db() 