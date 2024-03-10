from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas


async def get_tourist_spot(db: AsyncSession, tourist_spot_id: int):
    result = await db.execute(
        select(models.TouristSpot).filter(models.TouristSpot.id == tourist_spot_id)
    )
    return result.scalars().first()


async def get_tourist_spots(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.TouristSpot).offset(skip).limit(limit))
    return result.scalars().all()


async def create_tourist_spot(
    db: AsyncSession, tourist_spot: schemas.TouristSpotCreate
):
    db_tourist_spot = models.TouristSpot(**tourist_spot.model_dump())
    db.add(db_tourist_spot)
    await db.commit()
    await db.refresh(db_tourist_spot)
    return db_tourist_spot


async def update_tourist_spot(
    db: AsyncSession, tourist_spot: schemas.TouristSpotUpdate, tourist_spot_id: int
):
    db_tourist_spot = await get_tourist_spot(db, tourist_spot_id)
    if db_tourist_spot:
        update_data = tourist_spot.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tourist_spot, key, value)
        await db.commit()
        await db.refresh(db_tourist_spot)
    return db_tourist_spot


async def delete_tourist_spot(db: AsyncSession, tourist_spot_id: int):
    db_tourist_spot = await get_tourist_spot(db, tourist_spot_id)
    if db_tourist_spot:
        await db.delete(db_tourist_spot)
        await db.commit()
    return db_tourist_spot


async def search_tourist_spots(
    db: AsyncSession, keyword: str, skip: int = 0, limit: int = 100
):
    result = await db.execute(
        select(models.TouristSpot)
        .filter(
            models.TouristSpot.name.contains(keyword)
            | models.TouristSpot.location.contains(keyword)
            | models.TouristSpot.description.contains(keyword)
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
