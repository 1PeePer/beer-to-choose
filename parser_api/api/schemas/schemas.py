from pydantic import BaseModel
from typing import Optional

class ProductResponse(BaseModel):
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