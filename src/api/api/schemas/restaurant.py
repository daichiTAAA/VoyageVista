from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    location: str
    cuisine: str
    link_to_external_review: Optional[str] = None


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    cuisine: Optional[str] = None
    link_to_external_review: Optional[str] = None


class Restaurant(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True


class RestaurantOut(Restaurant):
    pass
