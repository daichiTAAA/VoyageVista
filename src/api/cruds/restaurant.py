from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas
from setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)


async def get_restaurant(db: AsyncSession, restaurant_id: int):
    logger.info(f"Fetching restaurant with ID {restaurant_id}")
    try:
        result = await db.execute(
            select(models.Restaurant).filter(models.Restaurant.id == restaurant_id)
        )
        restaurant = result.scalars().first()
        if restaurant:
            logger.info(f"Successfully fetched restaurant with ID {restaurant_id}")
        else:
            logger.warning(f"Restaurant with ID {restaurant_id} not found")
        return restaurant
    except Exception as e:
        logger.error(f"Error fetching restaurant with ID {restaurant_id}: {e}")
        raise


async def get_restaurants(db: AsyncSession, skip: int = 0, limit: int = 100):
    logger.info("Fetching list of restaurants")
    try:
        result = await db.execute(select(models.Restaurant).offset(skip).limit(limit))
        restaurants = result.scalars().all()
        logger.info("Successfully fetched list of restaurants")
        return restaurants
    except Exception as e:
        logger.error("Error fetching list of restaurants: ", e)
        raise


async def create_restaurant(db: AsyncSession, restaurant: schemas.RestaurantCreate):
    logger.info("Creating a new restaurant")
    try:
        db_restaurant = models.Restaurant(
            **restaurant.model_dump()
        )  # Use .model_dump() for Pydantic models instead of .model_dump()
        db.add(db_restaurant)
        await db.commit()
        await db.refresh(db_restaurant)
        logger.info(f"Successfully created restaurant: {db_restaurant.name}")
        return db_restaurant
    except Exception as e:
        logger.error("Error creating restaurant: ", e)
        raise


async def update_restaurant(
    db: AsyncSession, restaurant: schemas.RestaurantUpdate, restaurant_id: int
):
    logger.info(f"Updating restaurant with ID {restaurant_id}")
    try:
        db_restaurant = await get_restaurant(db, restaurant_id)
        if db_restaurant:
            update_data = restaurant.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_restaurant, key, value)
            await db.commit()
            await db.refresh(db_restaurant)
            logger.info(f"Successfully updated restaurant with ID {restaurant_id}")
        else:
            logger.warning(f"Restaurant with ID {restaurant_id} not found")
        return db_restaurant
    except Exception as e:
        logger.error(f"Error updating restaurant with ID {restaurant_id}: {e}")
        raise


async def delete_restaurant(db: AsyncSession, restaurant_id: int):
    logger.info(f"Deleting restaurant with ID {restaurant_id}")
    try:
        db_restaurant = await get_restaurant(db, restaurant_id)
        if db_restaurant:
            await db.delete(db_restaurant)
            await db.commit()
            logger.info(f"Successfully deleted restaurant with ID {restaurant_id}")
        else:
            logger.warning(f"Restaurant with ID {restaurant_id} not found")
    except Exception as e:
        logger.error(f"Error deleting restaurant with ID {restaurant_id}: {e}")
        raise


async def search_restaurants(
    db: AsyncSession, keyword: str, skip: int = 0, limit: int = 100
):
    logger.info(f"Searching for restaurants with keyword '{keyword}'")
    try:
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
        restaurants = result.scalars().all()
        logger.info(f"Found restaurants with keyword '{keyword}'")
        return restaurants
    except Exception as e:
        logger.error(f"Error searching for restaurants with keyword '{keyword}': {e}")
        raise
