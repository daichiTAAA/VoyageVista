from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas


async def get_translation(db: AsyncSession, translation_id: int):
    result = await db.execute(
        select(models.Translation).filter(models.Translation.id == translation_id)
    )
    return result.scalars().first()


async def get_translations(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Translation).offset(skip).limit(limit))
    return result.scalars().all()


async def create_translation(
    db: AsyncSession, translation: schemas.TranslationCreate, article_id: int
):
    db_translation = models.Translation(
        **translation.model_dump(), article_id=article_id
    )
    db.add(db_translation)
    await db.commit()
    await db.refresh(db_translation)
    return db_translation


async def update_translation(
    db: AsyncSession, translation: schemas.TranslationUpdate, translation_id: int
):
    db_translation = await get_translation(db, translation_id)
    if db_translation:
        update_data = translation.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_translation, key, value)
        await db.commit()
        await db.refresh(db_translation)
    return db_translation


async def delete_translation(db: AsyncSession, translation_id: int):
    db_translation = await get_translation(db, translation_id)
    if db_translation:
        await db.delete(db_translation)
        await db.commit()
    return db_translation


async def get_translations_by_article(
    db: AsyncSession, article_id: int, skip: int = 0, limit: int = 100
):
    result = await db.execute(
        select(models.Translation)
        .filter(models.Translation.article_id == article_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_translation_by_article_and_language(
    db: AsyncSession, article_id: int, language: str
):
    result = await db.execute(
        select(models.Translation).filter(
            models.Translation.article_id == article_id,
            models.Translation.language == language,
        )
    )
    return result.scalars().first()
