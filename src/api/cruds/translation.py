from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas
from setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)


async def get_translation(db: AsyncSession, translation_id: int):
    logger.info(f"Fetching translation with ID {translation_id}")
    try:
        result = await db.execute(
            select(models.Translation).filter(models.Translation.id == translation_id)
        )
        translation = result.scalars().first()
        logger.info(f"Successfully fetched translation with ID {translation_id}")
        return translation
    except Exception as e:
        logger.error(f"Error fetching translation with ID {translation_id}: {e}")
        raise


async def get_translations(db: AsyncSession, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching translations with skip {skip} and limit {limit}")
    try:
        result = await db.execute(select(models.Translation).offset(skip).limit(limit))
        translations = result.scalars().all()
        logger.info(
            f"Successfully fetched translations with skip {skip} and limit {limit}"
        )
        return translations
    except Exception as e:
        logger.error(f"Error fetching translations: {e}")
        raise


async def create_translation(
    db: AsyncSession, translation: schemas.TranslationCreate, article_id: int
):
    logger.info(f"Creating translation for article ID {article_id}")
    try:
        db_translation = models.Translation(
            **translation.model_dump(),
            article_id=article_id,
        )
        db.add(db_translation)
        await db.commit()
        await db.refresh(db_translation)
        logger.info(f"Successfully created translation for article ID {article_id}")
        return db_translation
    except Exception as e:
        logger.error(f"Error creating translation for article ID {article_id}: {e}")
        raise


async def update_translation(
    db: AsyncSession, translation: schemas.TranslationUpdate, translation_id: int
):
    logger.info(f"Updating translation with ID {translation_id}")
    try:
        db_translation = await get_translation(db, translation_id)
        if db_translation:
            update_data = translation.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_translation, key, value)
            await db.commit()
            await db.refresh(db_translation)
            logger.info(f"Successfully updated translation with ID {translation_id}")
            return db_translation
        else:
            logger.warning(f"Translation with ID {translation_id} not found")
    except Exception as e:
        logger.error(f"Error updating translation with ID {translation_id}: {e}")
        raise


async def delete_translation(db: AsyncSession, translation_id: int):
    logger.info(f"Deleting translation with ID {translation_id}")
    try:
        db_translation = await get_translation(db, translation_id)
        if db_translation:
            await db.delete(db_translation)
            await db.commit()
            logger.info(f"Successfully deleted translation with ID {translation_id}")
        else:
            logger.warning(f"Translation with ID {translation_id} not found")
    except Exception as e:
        logger.error(f"Error deleting translation with ID {translation_id}: {e}")
        raise


async def get_translations_by_article(
    db: AsyncSession, article_id: int, skip: int = 0, limit: int = 100
):
    logger.info(f"Fetching translations for article ID {article_id}")
    try:
        result = await db.execute(
            select(models.Translation)
            .filter(models.Translation.article_id == article_id)
            .offset(skip)
            .limit(limit)
        )
        logger.info(f"Successfully fetched translations for article ID {article_id}")
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Error fetching translations for article ID {article_id}: {e}")
        raise


async def get_translation_by_article_and_language(
    db: AsyncSession, article_id: int, language: str
):
    logger.info(
        f"Fetching translation for article ID {article_id} and language {language}"
    )
    try:
        result = await db.execute(
            select(models.Translation).filter(
                models.Translation.article_id == article_id,
                models.Translation.language == language,
            )
        )
        logger.info(
            f"Successfully fetched translation for article ID {article_id} and language {language}"
        )
        return result.scalars().first()
    except Exception as e:
        logger.error(
            f"Error fetching translation for article ID {article_id} and language {language}: {e}"
        )
        raise
