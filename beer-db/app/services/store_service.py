from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.store import Store
from typing import List, Optional

class StoreService:
    def __init__(self, db: Session):
        self.db = db

    def create_store(self, address: str, city: str) -> Store:
        """Create a new store"""
        store = Store(
            address=address,
            city=city,
            last_updated=datetime.utcnow(),
            is_active=True,
            popularity_score=0.0,
            update_frequency=60,
            request_count_24h=0,
            is_auto_update=True
        )
        self.db.add(store)
        self.db.commit()
        self.db.refresh(store)
        return store

    def get_store(self, store_id: int) -> Optional[Store]:
        """Get store by ID"""
        return self.db.query(Store).filter(Store.id == store_id).first()

    def get_store_by_address(self, address: str) -> Optional[Store]:
        """Get store by address"""
        return self.db.query(Store).filter(Store.address == address).first()

    def update_store(self, store_id: int, **kwargs) -> Optional[Store]:
        """Update store data"""
        store = self.get_store(store_id)
        if store:
            for key, value in kwargs.items():
                setattr(store, key, value)
            store.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(store)
        return store

    def update_popularity(self, store_id: int) -> Optional[Store]:
        """Update store popularity score"""
        store = self.get_store(store_id)
        if store:
            # Обновляем время последнего запроса
            store.last_request_time = datetime.utcnow()
            store.request_count_24h += 1

            # Рассчитываем популярность
            time_factor = 1.0
            if store.last_request_time:
                hours_since_last_request = (datetime.utcnow() - store.last_request_time).total_seconds() / 3600
                time_factor = max(0.1, 1.0 - (hours_since_last_request / 24))

            store.popularity_score = (
                store.request_count_24h * 0.4 +
                time_factor * 0.3 +
                (1.0 if store.is_auto_update else 0.0) * 0.3
            ) * 100

            # Обновляем частоту обновления
            if store.popularity_score > 80:
                store.update_frequency = 60
            elif store.popularity_score > 50:
                store.update_frequency = 180
            elif store.popularity_score > 20:
                store.update_frequency = 360
            else:
                store.update_frequency = 1440

            self.db.commit()
            self.db.refresh(store)
        return store

    def reset_daily_stats(self) -> None:
        """Reset daily statistics for all stores"""
        self.db.query(Store).update({
            "request_count_24h": 0,
            "popularity_score": 0.0
        })
        self.db.commit()

    def get_stores_for_update(self) -> List[Store]:
        """Get stores that need to be updated"""
        now = datetime.utcnow()
        return self.db.query(Store).filter(
            Store.is_active == True,
            Store.is_auto_update == True,
            (
                (Store.last_updated == None) |
                (now - Store.last_updated >= timedelta(minutes=Store.update_frequency))
            )
        ).all() 