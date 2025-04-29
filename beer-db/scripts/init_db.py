import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.config.database import SQLALCHEMY_DATABASE_URL

def init_db():
    """Initialize database"""
    # Создаем движок базы данных
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db() 