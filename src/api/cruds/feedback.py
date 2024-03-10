from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas


async def get_feedback(db: AsyncSession, feedback_id: int):
    result = await db.execute(
        select(models.Feedback).filter(models.Feedback.id == feedback_id)
    )
    return result.scalars().first()


async def get_feedbacks(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Feedback).offset(skip).limit(limit))
    return result.scalars().all()


async def create_feedback(
    db: AsyncSession, feedback: schemas.FeedbackCreate, user_id: int, article_id: int
):
    db_feedback = models.Feedback(
        **feedback.dict(), user_id=user_id, article_id=article_id
    )
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback


async def update_feedback(
    db: AsyncSession, feedback: schemas.FeedbackUpdate, feedback_id: int
):
    db_feedback = await get_feedback(db, feedback_id)
    if db_feedback:
        update_data = feedback.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_feedback, key, value)
        await db.commit()
        await db.refresh(db_feedback)
    return db_feedback


async def delete_feedback(db: AsyncSession, feedback_id: int):
    db_feedback = await get_feedback(db, feedback_id)
    if db_feedback:
        await db.delete(db_feedback)
        await db.commit()
    return db_feedback


async def get_feedbacks_by_article(
    db: AsyncSession, article_id: int, skip: int = 0, limit: int = 100
):
    result = await db.execute(
        select(models.Feedback)
        .filter(models.Feedback.article_id == article_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_feedbacks_by_user(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
):
    result = await db.execute(
        select(models.Feedback)
        .filter(models.Feedback.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
