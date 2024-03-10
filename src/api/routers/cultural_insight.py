from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import cruds, schemas
from db import SessionLocal

router_v1 = APIRouter(
    prefix="/cultural_insights",
    tags=["cultural_insights"],
    responses={404: {"description": "Not found"}},
)


async def get_db():
    async with SessionLocal() as session:
        yield session


@router_v1.post("/", response_model=schemas.CulturalInsight)
async def create_cultural_insight(
    cultural_insight: schemas.CulturalInsightCreate,
    article_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await cruds.create_cultural_insight(
        db=db, cultural_insight=cultural_insight, article_id=article_id
    )


@router_v1.get("/", response_model=List[schemas.CulturalInsight])
async def read_cultural_insights(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    cultural_insights = await cruds.get_cultural_insights(db, skip=skip, limit=limit)
    return cultural_insights


@router_v1.get("/{cultural_insight_id}", response_model=schemas.CulturalInsight)
async def read_cultural_insight(
    cultural_insight_id: int, db: AsyncSession = Depends(get_db)
):
    db_cultural_insight = await cruds.get_cultural_insight(
        db, cultural_insight_id=cultural_insight_id
    )
    if db_cultural_insight is None:
        raise HTTPException(status_code=404, detail="Cultural insight not found")
    return db_cultural_insight


@router_v1.put("/{cultural_insight_id}", response_model=schemas.CulturalInsight)
async def update_cultural_insight(
    cultural_insight_id: int,
    cultural_insight: schemas.CulturalInsightUpdate,
    db: AsyncSession = Depends(get_db),
):
    db_cultural_insight = await cruds.get_cultural_insight(
        db, cultural_insight_id=cultural_insight_id
    )
    if db_cultural_insight is None:
        raise HTTPException(status_code=404, detail="Cultural insight not found")
    return await cruds.update_cultural_insight(
        db=db,
        cultural_insight=cultural_insight,
        cultural_insight_id=cultural_insight_id,
    )


@router_v1.delete("/{cultural_insight_id}", response_model=schemas.CulturalInsight)
async def delete_cultural_insight(
    cultural_insight_id: int, db: AsyncSession = Depends(get_db)
):
    db_cultural_insight = await cruds.get_cultural_insight(
        db, cultural_insight_id=cultural_insight_id
    )
    if db_cultural_insight is None:
        raise HTTPException(status_code=404, detail="Cultural insight not found")
    return await cruds.delete_cultural_insight(
        db=db, cultural_insight_id=cultural_insight_id
    )
