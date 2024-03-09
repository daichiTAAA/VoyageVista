from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import cruds, schemas
from db import SessionLocal

router = APIRouter(
    prefix="/cultural_insights",
    tags=["cultural_insights"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.CulturalInsight)
def create_cultural_insight(
    cultural_insight: schemas.CulturalInsightCreate,
    article_id: int,
    db: Session = Depends(get_db),
):
    return cruds.create_cultural_insight(
        db=db, cultural_insight=cultural_insight, article_id=article_id
    )


@router.get("/", response_model=List[schemas.CulturalInsight])
def read_cultural_insights(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    cultural_insights = cruds.get_cultural_insights(db, skip=skip, limit=limit)
    return cultural_insights


@router.get("/{cultural_insight_id}", response_model=schemas.CulturalInsight)
def read_cultural_insight(cultural_insight_id: int, db: Session = Depends(get_db)):
    db_cultural_insight = cruds.get_cultural_insight(
        db, cultural_insight_id=cultural_insight_id
    )
    if db_cultural_insight is None:
        raise HTTPException(status_code=404, detail="Cultural insight not found")
    return db_cultural_insight


@router.put("/{cultural_insight_id}", response_model=schemas.CulturalInsight)
def update_cultural_insight(
    cultural_insight_id: int,
    cultural_insight: schemas.CulturalInsightCreate,
    db: Session = Depends(get_db),
):
    db_cultural_insight = cruds.get_cultural_insight(
        db, cultural_insight_id=cultural_insight_id
    )
    if db_cultural_insight is None:
        raise HTTPException(status_code=404, detail="Cultural insight not found")
    return cruds.update_cultural_insight(
        db=db,
        cultural_insight=cultural_insight,
        cultural_insight_id=cultural_insight_id,
    )


@router.delete("/{cultural_insight_id}", response_model=schemas.CulturalInsight)
def delete_cultural_insight(cultural_insight_id: int, db: Session = Depends(get_db)):
    db_cultural_insight = cruds.get_cultural_insight(
        db, cultural_insight_id=cultural_insight_id
    )
    if db_cultural_insight is None:
        raise HTTPException(status_code=404, detail="Cultural insight not found")
    return cruds.delete_cultural_insight(db=db, cultural_insight_id=cultural_insight_id)
