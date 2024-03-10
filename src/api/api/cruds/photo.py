from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import UploadFile

import api.models as models
import api.schemas as schemas
from api.setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)


async def get_photo(db: AsyncSession, photo_id: int):
    logger.info(f"Fetching photo with ID {photo_id}")
    try:
        result = await db.execute(
            select(models.Photo).filter(models.Photo.id == photo_id)
        )
        photo = result.scalars().first()
        if photo:
            logger.info(f"Successfully fetched photo with ID {photo_id}")
        else:
            logger.warning(f"Photo with ID {photo_id} not found")
        return photo
    except Exception as e:
        logger.error(f"Error fetching photo with ID {photo_id}: {e}")
        raise


async def get_photos(db: AsyncSession, skip: int = 0, limit: int = 100):
    logger.info("Fetching list of photos")
    try:
        result = await db.execute(select(models.Photo).offset(skip).limit(limit))
        photos = result.scalars().all()
        logger.info("Successfully fetched list of photos")
        return photos
    except Exception as e:
        logger.error("Error fetching list of photos: ", e)
        raise


async def create_photo(db: AsyncSession, photo: schemas.PhotoCreate, article_id: int):
    logger.info(f"Creating a new photo for article ID {article_id}")
    try:
        db_photo = models.Photo(
            **photo.model_dump(),
            article_id=article_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(db_photo)
        await db.commit()
        await db.refresh(db_photo)
        logger.info(f"Successfully created photo: {photo.file_path}")
        return db_photo
    except Exception as e:
        logger.error("Error creating photo: ", e)
        raise


async def update_photo(db: AsyncSession, photo: schemas.PhotoUpdate, photo_id: int):
    logger.info(f"Updating photo with ID {photo_id}")
    try:
        db_photo = await get_photo(db, photo_id)
        if db_photo:
            update_data = {
                **photo.model_dump(exclude_unset=True),
                "updated_at": datetime.now(),
            }
            for key, value in update_data.items():
                setattr(db_photo, key, value)
            db_photo.file_path = photo.file_path
            db_photo.description = photo.description
            await db.commit()
            await db.refresh(db_photo)
            logger.info(f"Successfully updated photo with ID {photo_id}")
        else:
            logger.warning(f"Photo with ID {photo_id} not found")
        return db_photo
    except Exception as e:
        logger.error(f"Error updating photo with ID {photo_id}: {e}")
        raise


async def delete_photo(db: AsyncSession, photo_id: int):
    logger.info(f"Deleting photo with ID {photo_id}")
    try:
        db_photo = await get_photo(db, photo_id)
        if db_photo:
            await db.delete(db_photo)
            await db.commit()
            logger.info(f"Successfully deleted photo with ID {photo_id}")
        else:
            logger.warning(f"Photo with ID {photo_id} not found")
    except Exception as e:
        logger.error(f"Error deleting photo with ID {photo_id}: {e}")
        raise


async def get_photos_by_article(
    db: AsyncSession, article_id: int, skip: int = 0, limit: int = 100
):
    logger.info(f"Fetching photos for article ID {article_id}")
    try:
        result = await db.execute(
            select(models.Photo)
            .filter(models.Photo.article_id == article_id)
            .offset(skip)
            .limit(limit)
        )
        photos = result.scalars().all()
        logger.info(f"Successfully fetched photos for article ID {article_id}")
        return photos
    except Exception as e:
        logger.error(f"Error fetching photos for article ID {article_id}: {e}")
        raise
