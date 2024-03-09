from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import cruds, schemas
from db import SessionLocal

router = APIRouter(
    prefix="/feedbacks",
    tags=["feedbacks"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Feedback)
def create_feedback(
    feedback: schemas.FeedbackCreate,
    user_id: int,
    article_id: int,
    db: Session = Depends(get_db),
):
    return cruds.create_feedback(
        db=db, feedback=feedback, user_id=user_id, article_id=article_id
    )


@router.get("/", response_model=List[schemas.Feedback])
def read_feedbacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feedbacks = cruds.get_feedbacks(db, skip=skip, limit=limit)
    return feedbacks


@router.get("/{feedback_id}", response_model=schemas.Feedback)
def read_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = cruds.get_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return db_feedback


@router.put("/{feedback_id}", response_model=schemas.Feedback)
def update_feedback(
    feedback_id: int, feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)
):
    db_feedback = cruds.get_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return cruds.update_feedback(db=db, feedback=feedback, feedback_id=feedback_id)


@router.delete("/{feedback_id}", response_model=schemas.Feedback)
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = cruds.get_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return cruds.delete_feedback(db=db, feedback_id=feedback_id)
