from sqlalchemy import Column, String, Float, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class ProductType(enum.Enum):
    BEER = "Пиво"
    CIDER = "Сидр"
    MEAD = "Медовуха"
    DRINK = "Напиток"
    UNKNOWN = "Неизвестный тип"

class FilteringType(enum.Enum):
    FILTERED = "Фильтрованное"
    UNFILTERED = "Нефильтрованное"
    UNKNOWN = "unknown"

class PasteurizationType(enum.Enum):
    PASTEURIZED = "Пастеризованное"
    UNPASTEURIZED = "Непастеризованное"
    UNKNOWN = "unknown"

class SweetnessType(enum.Enum):
    SWEET = "Сладкое"
    SEMI_SWEET = "Полусладкое"
    SEMI_DRY = "Полусухое"
    DRY = "Сухое"
    UNKNOWN = "unknown"

class PackagingType(enum.Enum):
    GLASS_BOTTLE = "с/б"
    PET = "ПЭТ"
    ALUMINUM_CAN = "ж/б"
    UNKNOWN = "unknown"

class ClarificationType(enum.Enum):
    CLEAR = "Осветленное"
    HAZY = "Неосветленное"
    UNKNOWN = "unknown"

class Product(BaseModel):
    """Product model"""
    __tablename__ = "products"

    name = Column(String, nullable=False, index=True)
    type = Column(Enum(ProductType), nullable=False)
    color = Column(String, nullable=True)
    is_alcoholic = Column(Boolean, default=True)
    filtering = Column(Enum(FilteringType), nullable=True)
    pasteurization = Column(Enum(PasteurizationType), nullable=True)
    alcohol_percentage = Column(Float, nullable=True)
    sweetness = Column(Enum(SweetnessType), nullable=True)
    packaging = Column(Enum(PackagingType), nullable=True)
    clarification = Column(Enum(ClarificationType), nullable=True)
    volume = Column(String, nullable=False)
    price = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    last_updated = Column(DateTime, nullable=True)

    # Relationships
    stores = relationship("StoreProduct", back_populates="product") 