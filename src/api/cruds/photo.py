import os
import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import UploadFile

import models, schemas
from setup_logger import setup_logger

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


async def create_photo(db: AsyncSession, photo: UploadFile, article_id: int):
    logger.info(f"Creating a new photo for article ID {article_id}")
    file_path = f"photos/{photo.filename}"
    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            data = await photo.read()
            await buffer.write(data)

        db_photo = models.Photo(file_path=file_path, article_id=article_id)
        db.add(db_photo)
        await db.commit()
        await db.refresh(db_photo)
        logger.info(f"Successfully created photo: {file_path}")
        return db_photo
    except Exception as e:
        logger.error("Error creating photo: ", e)
        raise


async def update_photo(db: AsyncSession, photo: UploadFile, photo_id: int):
    logger.info(f"Updating photo with ID {photo_id}")
    try:
        db_photo = await get_photo(db, photo_id)
        if db_photo:
            file_path = f"photos/{photo.filename}"
            async with aiofiles.open(file_path, "wb") as buffer:
                data = await photo.read()
                await buffer.write(data)

            db_photo.file_path = file_path
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
            file_path = db_photo.file_path
            if os.path.exists(file_path):
                await aiofiles.os.remove(file_path)
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
