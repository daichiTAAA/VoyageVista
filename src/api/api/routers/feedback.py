from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import api.schemas as schemas
import api.cruds as cruds
from api.db import get_db
from api.setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)

router_v1 = APIRouter(
    prefix="/feedbacks",
    tags=["feedbacks"],
    responses={404: {"description": "Not found"}},
)


@router_v1.post(
    "/", response_model=schemas.Feedback, status_code=status.HTTP_201_CREATED
)
async def create_feedback(
    feedback: schemas.FeedbackCreate,
    user_id: int,
    article_id: int,
    db: AsyncSession = Depends(get_db),
):
    db_feedback = await cruds.create_feedback(
        db=db, feedback=feedback, user_id=user_id, article_id=article_id
    )
    if not db_feedback:
        logger.error("Feedback could not be created")
        raise HTTPException(status_code=400, detail="Feedback could not be created")
    return db_feedback


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
    success = await cruds.delete_feedback(db=db, feedback_id=feedback_id)
    if not success:
        logger.error(f"Feedback {feedback_id} not found")
        raise HTTPException(status_code=404, detail="Feedback not found")
    # 204 No Content ステータスコードを返すためにレスポンスボディは空
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)
