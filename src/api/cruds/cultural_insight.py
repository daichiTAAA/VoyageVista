from sqlalchemy.orm import Session

import models, schemas


def get_cultural_insight(db: Session, cultural_insight_id: int):
    return (
        db.query(models.CulturalInsight)
        .filter(models.CulturalInsight.id == cultural_insight_id)
        .first()
    )


def get_cultural_insights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CulturalInsight).offset(skip).limit(limit).all()


def create_cultural_insight(
    db: Session, cultural_insight: schemas.CulturalInsightCreate, article_id: int
):
    db_cultural_insight = models.CulturalInsight(
        **cultural_insight.model_dump(), article_id=article_id
    )
    db.add(db_cultural_insight)
    db.commit()
    db.refresh(db_cultural_insight)
    return db_cultural_insight


def update_cultural_insight(
    db: Session,
    cultural_insight: schemas.CulturalInsightUpdate,
    cultural_insight_id: int,
):
    db_cultural_insight = get_cultural_insight(db, cultural_insight_id)
    if db_cultural_insight:
        update_data = cultural_insight.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_cultural_insight, key, value)
        db.commit()
        db.refresh(db_cultural_insight)
    return db_cultural_insight


def delete_cultural_insight(db: Session, cultural_insight_id: int):
    db_cultural_insight = get_cultural_insight(db, cultural_insight_id)
    if db_cultural_insight:
        db.delete(db_cultural_insight)
        db.commit()
    return db_cultural_insight


def get_cultural_insights_by_article(
    db: Session, article_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.CulturalInsight)
        .filter(models.CulturalInsight.article_id == article_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
