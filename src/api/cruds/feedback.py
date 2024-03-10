from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas
from setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)


async def get_feedback(db: AsyncSession, feedback_id: int):
    logger.info(f"Fetching feedback with ID {feedback_id}")
    try:
        result = await db.execute(
            select(models.Feedback).filter(models.Feedback.id == feedback_id)
        )
        feedback = result.scalars().first()
        if feedback:
            logger.info(f"Successfully fetched feedback with ID {feedback_id}")
        else:
            logger.warning(f"Feedback with ID {feedback_id} not found")
        return feedback
    except Exception as e:
        logger.error(f"Error fetching feedback with ID {feedback_id}: {e}")
        raise


async def get_feedbacks(db: AsyncSession, skip: int = 0, limit: int = 100):
    logger.info("Fetching list of feedbacks")
    try:
        result = await db.execute(select(models.Feedback).offset(skip).limit(limit))
        feedbacks = result.scalars().all()
        logger.info("Successfully fetched list of feedbacks")
        return feedbacks
    except Exception as e:
        logger.error("Error fetching list of feedbacks: ", e)
        raise


async def create_feedback(
    db: AsyncSession, feedback: schemas.FeedbackCreate, user_id: int, article_id: int
):
    logger.info(
        f"Creating new feedback for article ID {article_id} by user ID {user_id}"
    )
    try:
        db_feedback = models.Feedback(
            **feedback.model_dump(), user_id=user_id, article_id=article_id
        )
        db.add(db_feedback)
        await db.commit()
        await db.refresh(db_feedback)
        logger.info("Successfully created new feedback")
        return db_feedback
    except Exception as e:
        logger.error("Error creating new feedback: ", e)
        raise


async def update_feedback(
    db: AsyncSession, feedback: schemas.FeedbackUpdate, feedback_id: int
):
    logger.info(f"Updating feedback with ID {feedback_id}")
    try:
        db_feedback = await get_feedback(db, feedback_id)
        if db_feedback:
            update_data = feedback.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_feedback, key, value)
            await db.commit()
            await db.refresh(db_feedback)
            logger.info(f"Successfully updated feedback with ID {feedback_id}")
        else:
            logger.warning(f"Feedback with ID {feedback_id} not found")
        return db_feedback
    except Exception as e:
        logger.error(f"Error updating feedback with ID {feedback_id}: {e}")
        raise


async def delete_feedback(db: AsyncSession, feedback_id: int):
    logger.info(f"Deleting feedback with ID {feedback_id}")
    try:
        db_feedback = await get_feedback(db, feedback_id)
        if db_feedback:
            await db.delete(db_feedback)
            await db.commit()
            logger.info(f"Successfully deleted feedback with ID {feedback_id}")
        else:
            logger.warning(f"Feedback with ID {feedback_id} not found")
    except Exception as e:
        logger.error(f"Error deleting feedback with ID {feedback_id}: {e}")
        raise


async def get_feedbacks_by_article(
    db: AsyncSession, article_id: int, skip: int = 0, limit: int = 100
):
    logger.info(f"Fetching feedbacks for article ID {article_id}")
    try:
        result = await db.execute(
            select(models.Feedback)
            .filter(models.Feedback.article_id == article_id)
            .offset(skip)
            .limit(limit)
        )
        feedbacks = result.scalars().all()
        logger.info(f"Successfully fetched feedbacks for article ID {article_id}")
        return feedbacks
    except Exception as e:
        logger.error(f"Error fetching feedbacks for article ID {article_id}: {e}")
        raise


async def get_feedbacks_by_user(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
):
    logger.info(f"Fetching feedbacks for user ID {user_id}")
    try:
        result = await db.execute(
            select(models.Feedback)
            .filter(models.Feedback.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        feedbacks = result.scalars().all()
        logger.info(f"Successfully fetched feedbacks for user ID {user_id}")
        return feedbacks
    except Exception as e:
        logger.error(f"Error fetching feedbacks for user ID {user_id}: {e}")
        raise
