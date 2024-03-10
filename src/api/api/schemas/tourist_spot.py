from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TouristSpotBase(BaseModel):
    name: str
    location: str
    description: str
    average_stay_time: float


class TouristSpotCreate(TouristSpotBase):
    pass


class TouristSpotUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    average_stay_time: Optional[float] = None


class TouristSpot(TouristSpotBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True


class TouristSpotOut(TouristSpot):
    pass
