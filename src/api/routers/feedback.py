from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import cruds, schemas
from db import SessionLocal
from setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)

router_v1 = APIRouter(
    prefix="/feedbacks",
    tags=["feedbacks"],
    responses={404: {"description": "Not found"}},
)


async def get_db():
    async with SessionLocal() as session:
        yield session


@router_v1.post("/", response_model=schemas.Feedback)
async def create_feedback(
    feedback: schemas.FeedbackCreate,
    user_id: int,
    article_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await cruds.create_feedback(
        db=db, feedback=feedback, user_id=user_id, article_id=article_id
    )


@router_v1.get("/", response_model=List[schemas.Feedback])
async def read_feedbacks(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    feedbacks = await cruds.get_feedbacks(db, skip=skip, limit=limit)
    return feedbacks


@router_v1.get("/{feedback_id}", response_model=schemas.Feedback)
async def read_feedback(feedback_id: int, db: AsyncSession = Depends(get_db)):
    db_feedback = await cruds.get_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        logger.error(f"Feedback {feedback_id} not found")
        raise HTTPException(status_code=404, detail="Feedback not found")
    return db_feedback


@router_v1.put("/{feedback_id}", response_model=schemas.Feedback)
async def update_feedback(
    feedback_id: int,
    feedback: schemas.FeedbackUpdate,
    db: AsyncSession = Depends(get_db),
):
    db_feedback = await cruds.get_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        logger.error(f"Feedback {feedback_id} not found")
        raise HTTPException(status_code=404, detail="Feedback not found")
    return await cruds.update_feedback(
        db=db, feedback=feedback, feedback_id=feedback_id
    )


@router_v1.delete("/{feedback_id}", response_model=schemas.Feedback)
async def delete_feedback(feedback_id: int, db: AsyncSession = Depends(get_db)):
    db_feedback = await cruds.get_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        logger.error(f"Feedback {feedback_id} not found")
        raise HTTPException(status_code=404, detail="Feedback not found")
    return await cruds.delete_feedback(db=db, feedback_id=feedback_id)
