from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas
from setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)


async def get_tourist_spot(db: AsyncSession, tourist_spot_id: int):
    logger.info(f"Fetching tourist spot with ID {tourist_spot_id}")
    try:
        result = await db.execute(
            select(models.TouristSpot).filter(models.TouristSpot.id == tourist_spot_id)
        )
        tourist_spot = result.scalars().first()
        logger.info(f"Successfully fetched tourist spot with ID {tourist_spot_id}")
        return tourist_spot
    except Exception as e:
        logger.error(f"Error fetching tourist spot with ID {tourist_spot_id}: {e}")
        raise


async def get_tourist_spots(db: AsyncSession, skip: int = 0, limit: int = 100):
    logger.info("Fetching tourist spots")
    try:
        result = await db.execute(select(models.TouristSpot).offset(skip).limit(limit))
        tourist_spots = result.scalars().all()
        logger.info("Successfully fetched tourist spots")
        return tourist_spots
    except Exception as e:
        logger.error(f"Error fetching tourist spots: {e}")
        raise


async def create_tourist_spot(
    db: AsyncSession, tourist_spot: schemas.TouristSpotCreate
):
    logger.info("Creating a new tourist spot")
    try:
        db_tourist_spot = models.TouristSpot(**tourist_spot.model_dump())
        db.add(db_tourist_spot)
        await db.commit()
        await db.refresh(db_tourist_spot)
        logger.info("Successfully created a new tourist spot")
        return db_tourist_spot
    except Exception as e:
        logger.error(f"Error creating tourist spot: {e}")
        raise


async def update_tourist_spot(
    db: AsyncSession, tourist_spot: schemas.TouristSpotUpdate, tourist_spot_id: int
):
    logger.info(f"Updating tourist spot with ID {tourist_spot_id}")
    try:
        db_tourist_spot = await get_tourist_spot(db, tourist_spot_id)
        if db_tourist_spot:
            update_data = tourist_spot.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_tourist_spot, key, value)
            await db.commit()
            await db.refresh(db_tourist_spot)
            logger.info(f"Successfully updated tourist spot with ID {tourist_spot_id}")
            return db_tourist_spot
        else:
            logger.warning(f"Tourist spot with ID {tourist_spot_id} not found")
    except Exception as e:
        logger.error(f"Error updating tourist spot with ID {tourist_spot_id}: {e}")
        raise


async def delete_tourist_spot(db: AsyncSession, tourist_spot_id: int):
    logger.info(f"Deleting tourist spot with ID {tourist_spot_id}")
    try:
        db_tourist_spot = await get_tourist_spot(db, tourist_spot_id)
        if db_tourist_spot:
            await db.delete(db_tourist_spot)
            await db.commit()
            logger.info(f"Successfully deleted tourist spot with ID {tourist_spot_id}")
        else:
            logger.warning(f"Tourist spot with ID {tourist_spot_id} not found")
    except Exception as e:
        logger.error(f"Error deleting tourist spot with ID {tourist_spot_id}: {e}")
        raise


async def search_tourist_spots(
    db: AsyncSession, keyword: str, skip: int = 0, limit: int = 100
):
    logger.info(f"Searching for tourist spots with keyword '{keyword}'")
    try:
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
        tourist_spots = result.scalars().all()
        logger.info(f"Found tourist spots with keyword '{keyword}'")
        return tourist_spots
    except Exception as e:
        logger.error(f"Error searching for tourist spots with keyword '{keyword}': {e}")
        raise
