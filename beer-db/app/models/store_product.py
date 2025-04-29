from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class StoreProduct(BaseModel):
    """Store-Product relationship model"""
    __tablename__ = "store_products"

    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    is_available = Column(Boolean, default=True)
    last_updated = Column(DateTime, nullable=True)

    # Relationships
    store = relationship("Store", back_populates="products")
    product = relationship("Product", back_populates="stores") 