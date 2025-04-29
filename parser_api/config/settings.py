from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Beer Parser API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for beer products parsing and management"
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "logs/api.log"
    
    # Parser settings
    DEFAULT_ADDRESS: str = "Москва, Чонгарский бул., 7"
    TIMEOUT: int = 30000
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 