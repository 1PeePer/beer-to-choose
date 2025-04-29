from datetime import datetime
from sqlalchemy.orm import Session
from ..models.product import Product, ProductType
from ..models.store_product import StoreProduct
from typing import List, Optional, Dict

class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, **kwargs) -> Product:
        """Create a new product"""
        product = Product(**kwargs)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_product(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.db.query(Product).filter(Product.id == product_id).first()

    def update_product(self, product_id: int, **kwargs) -> Optional[Product]:
        """Update product data"""
        product = self.get_product(product_id)
        if product:
            for key, value in kwargs.items():
                setattr(product, key, value)
            product.last_updated = datetime.utcnow()
            self.db.commit()
            self.db.refresh(product)
        return product

    def get_products_by_store(self, store_id: int) -> List[Product]:
        """Get all products available in a store"""
        return self.db.query(Product).join(StoreProduct).filter(
            StoreProduct.store_id == store_id,
            StoreProduct.is_available == True
        ).all()

    def update_store_products(self, store_id: int, products: List[Dict]) -> None:
        """Update products availability in a store"""
        # Получаем все существующие связи
        existing_links = self.db.query(StoreProduct).filter(
            StoreProduct.store_id == store_id
        ).all()
        existing_product_ids = {link.product_id for link in existing_links}

        # Обновляем существующие связи
        for link in existing_links:
            product_data = next(
                (p for p in products if p["name"] == link.product.name),
                None
            )
            if product_data:
                link.is_available = True
                link.last_updated = datetime.utcnow()
            else:
                link.is_available = False
                link.last_updated = datetime.utcnow()

        # Добавляем новые связи
        for product_data in products:
            product = self.db.query(Product).filter(
                Product.name == product_data["name"]
            ).first()

            if not product:
                product = self.create_product(**product_data)

            if product.id not in existing_product_ids:
                store_product = StoreProduct(
                    store_id=store_id,
                    product_id=product.id,
                    is_available=True,
                    last_updated=datetime.utcnow()
                )
                self.db.add(store_product)

        self.db.commit()

    def search_products(self, query: str, store_id: Optional[int] = None) -> List[Product]:
        """Search products by name"""
        q = self.db.query(Product)
        if store_id:
            q = q.join(StoreProduct).filter(
                StoreProduct.store_id == store_id,
                StoreProduct.is_available == True
            )
        return q.filter(Product.name.ilike(f"%{query}%")).all()

    def filter_products(
        self,
        store_id: Optional[int] = None,
        product_type: Optional[ProductType] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_alcohol: Optional[float] = None,
        max_alcohol: Optional[float] = None
    ) -> List[Product]:
        """Filter products by various criteria"""
        q = self.db.query(Product)
        
        if store_id:
            q = q.join(StoreProduct).filter(
                StoreProduct.store_id == store_id,
                StoreProduct.is_available == True
            )
        
        if product_type:
            q = q.filter(Product.type == product_type)
        
        if min_price is not None:
            q = q.filter(Product.price >= min_price)
        
        if max_price is not None:
            q = q.filter(Product.price <= max_price)
        
        if min_alcohol is not None:
            q = q.filter(Product.alcohol >= min_alcohol)
        
        if max_alcohol is not None:
            q = q.filter(Product.alcohol <= max_alcohol)
        
        return q.all() 