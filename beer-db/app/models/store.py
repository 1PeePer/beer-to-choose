from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class Store(BaseModel):
    """Store model"""
    __tablename__ = "stores"

    address = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    last_updated = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    popularity_score = Column(Float, default=0.0)
    update_frequency = Column(Integer, default=60)  # в минутах
    last_request_time = Column(DateTime, nullable=True)
    request_count_24h = Column(Integer, default=0)
    is_auto_update = Column(Boolean, default=True)

    # Relationships
    products = relationship("StoreProduct", back_populates="store") 