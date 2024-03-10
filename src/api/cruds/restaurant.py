from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas


async def get_restaurant(db: AsyncSession, restaurant_id: int):
    result = await db.execute(
        select(models.Restaurant).filter(models.Restaurant.id == restaurant_id)
    )
    return result.scalars().first()


async def get_restaurants(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Restaurant).offset(skip).limit(limit))
    return result.scalars().all()


async def create_restaurant(db: AsyncSession, restaurant: schemas.RestaurantCreate):
    db_restaurant = models.Restaurant(**restaurant.model_dump())
    db.add(db_restaurant)
    await db.commit()
    await db.refresh(db_restaurant)
    return db_restaurant


async def update_restaurant(
    db: AsyncSession, restaurant: schemas.RestaurantUpdate, restaurant_id: int
):
    db_restaurant = await get_restaurant(db, restaurant_id)
    if db_restaurant:
        update_data = restaurant.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_restaurant, key, value)
        await db.commit()
        await db.refresh(db_restaurant)
    return db_restaurant


async def delete_restaurant(db: AsyncSession, restaurant_id: int):
    db_restaurant = await get_restaurant(db, restaurant_id)
    if db_restaurant:
        await db.delete(db_restaurant)
        await db.commit()
    return db_restaurant


async def search_restaurants(
    db: AsyncSession, keyword: str, skip: int = 0, limit: int = 100
):
    result = await db.execute(
        select(models.Restaurant)
        .filter(
            models.Restaurant.name.contains(keyword)
            | models.Restaurant.location.contains(keyword)
            | models.Restaurant.cuisine.contains(keyword)
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
