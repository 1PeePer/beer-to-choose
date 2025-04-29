import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.services.store_service import StoreService
from app.services.product_service import ProductService

def check_db():
    """Check database data"""
    db = SessionLocal()
    try:
        # Проверяем магазины
        store_service = StoreService(db)
        stores = store_service.get_stores_for_update()
        print("\n=== Магазины ===")
        for store in stores:
            print(f"ID: {store.id}")
            print(f"Адрес: {store.address}")
            print(f"Город: {store.city}")
            print(f"Последнее обновление: {store.last_updated}")
            print(f"Популярность: {store.popularity_score}")
            print(f"Частота обновления: {store.update_frequency} минут")
            print("---")

        # Проверяем товары
        product_service = ProductService(db)
        for store in stores:
            print(f"\n=== Товары в магазине {store.address} ===")
            products = product_service.get_products_by_store(store.id)
            for product in products:
                print(f"ID: {product.id}")
                print(f"Название: {product.name}")
                print(f"Тип: {product.type.value}")
                print(f"Цвет: {product.color}")
                print(f"Алкоголь: {product.alcohol_percentage}%")
                print(f"Объем: {product.volume}")
                print(f"Цена: {product.price}")
                print("---")

    finally:
        db.close()

if __name__ == "__main__":
    check_db() 