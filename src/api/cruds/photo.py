import os
import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import UploadFile

import models, schemas


async def get_photo(db: AsyncSession, photo_id: int):
    result = await db.execute(select(models.Photo).filter(models.Photo.id == photo_id))
    return result.scalars().first()


async def get_photos(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Photo).offset(skip).limit(limit))
    return result.scalars().all()


async def create_photo(db: AsyncSession, photo: UploadFile, article_id: int):
    file_path = f"photos/{photo.filename}"
    async with aiofiles.open(file_path, "wb") as buffer:
        data = await photo.read()
        await buffer.write(data)

    db_photo = models.Photo(file_path=file_path, article_id=article_id)
    db.add(db_photo)
    await db.commit()
    await db.refresh(db_photo)
    return db_photo


async def update_photo(db: AsyncSession, photo: UploadFile, photo_id: int):
    db_photo = await get_photo(db, photo_id)
    if db_photo:
        file_path = f"photos/{photo.filename}"
        async with aiofiles.open(file_path, "wb") as buffer:
            data = await photo.read()
            await buffer.write(data)

        db_photo.file_path = file_path
        await db.commit()
        await db.refresh(db_photo)
    return db_photo


async def delete_photo(db: AsyncSession, photo_id: int):
    db_photo = await get_photo(db, photo_id)
    if db_photo:
        file_path = db_photo.file_path
        if os.path.exists(file_path):
            await aiofiles.os.remove(file_path)
        await db.delete(db_photo)
        await db.commit()
    return db_photo


async def get_photos_by_article(
    db: AsyncSession, article_id: int, skip: int = 0, limit: int = 100
):
    result = await db.execute(
        select(models.Photo)
        .filter(models.Photo.article_id == article_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
