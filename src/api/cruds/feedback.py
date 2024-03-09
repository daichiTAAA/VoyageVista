from sqlalchemy.orm import Session

import models, schemas


def get_feedback(db: Session, feedback_id: int):
    return db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()


def get_feedbacks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Feedback).offset(skip).limit(limit).all()


def create_feedback(
    db: Session, feedback: schemas.FeedbackCreate, user_id: int, article_id: int
):
    db_feedback = models.Feedback(
        **feedback.model_dump(), user_id=user_id, article_id=article_id
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


def update_feedback(db: Session, feedback: schemas.FeedbackUpdate, feedback_id: int):
    db_feedback = get_feedback(db, feedback_id)
    if db_feedback:
        update_data = feedback.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_feedback, key, value)
        db.commit()
        db.refresh(db_feedback)
    return db_feedback


def delete_feedback(db: Session, feedback_id: int):
    db_feedback = get_feedback(db, feedback_id)
    if db_feedback:
        db.delete(db_feedback)
        db.commit()
    return db_feedback


def get_feedbacks_by_article(
    db: Session, article_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Feedback)
        .filter(models.Feedback.article_id == article_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_feedbacks_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Feedback)
        .filter(models.Feedback.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
