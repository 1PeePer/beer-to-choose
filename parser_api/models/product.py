from typing import Optional
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    type: str
    color: Optional[str] = None
    is_alcoholic: bool = True
    filtering: Optional[str] = None
    pasteurization: Optional[str] = None
    alcohol_percentage: Optional[float] = None
    sweetness: Optional[str] = None
    packaging: str = "с/б"
    clarification: Optional[str] = None
    volume: str = "0.33L"
    price: str = "0.00 ₽"
    image: str = "https://sitecdn.api.lenta.com/assets-ng/empty-image.svg"

    def to_dict(self) -> dict:
        """Convert product to dictionary"""
        return {
            "name": self.name,
            "type": self.type,
            "color": self.color,
            "is_alcoholic": self.is_alcoholic,
            "filtering": self.filtering,
            "pasteurization": self.pasteurization,
            "alcohol_percentage": self.alcohol_percentage,
            "sweetness": self.sweetness,
            "packaging": self.packaging,
            "clarification": self.clarification,
            "volume": self.volume,
            "price": self.price,
            "image": self.image
        } 