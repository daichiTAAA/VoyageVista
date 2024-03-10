from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import api.schemas as schemas
import api.cruds as cruds
from api.db import get_db
from api.setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)

router_v1 = APIRouter(
    prefix="/cultural_insights",
    tags=["cultural_insights"],
    responses={404: {"description": "Not found"}},
)


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
        logger.error(f"Cultural insight {cultural_insight_id} not found")
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
        logger.error(f"Cultural insight {cultural_insight_id} not found")
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
        logger.error(f"Cultural insight {cultural_insight_id} not found")
        raise HTTPException(status_code=404, detail="Cultural insight not found")
    success = await cruds.delete_cultural_insight(
        db=db, cultural_insight_id=cultural_insight_id
    )
    if not success:
        logger.error(f"Cultural insight {cultural_insight_id} not found")
        raise HTTPException(status_code=404, detail="Article not found")
    # 204 No Content ステータスコードを返すためにレスポンスボディは空
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)
