from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import api.cruds as cruds
from api.db import get_db

import api.schemas as schemas
from api.setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)

router_v1 = APIRouter(
    prefix="/tourist_spots",
    tags=["tourist_spots"],
    responses={404: {"description": "Not found"}},
)


@router_v1.post("/", response_model=schemas.TouristSpot)
async def create_tourist_spot(
    tourist_spot: schemas.TouristSpotCreate, db: AsyncSession = Depends(get_db)
):
    return await cruds.create_tourist_spot(db=db, tourist_spot=tourist_spot)


@router_v1.get("/", response_model=List[schemas.TouristSpot])
async def read_tourist_spots(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await cruds.get_tourist_spots(db, skip=skip, limit=limit)


@router_v1.get("/{tourist_spot_id}", response_model=schemas.TouristSpot)
async def read_tourist_spot(tourist_spot_id: int, db: AsyncSession = Depends(get_db)):
    db_tourist_spot = await cruds.get_tourist_spot(db, tourist_spot_id=tourist_spot_id)
    if db_tourist_spot is None:
        logger.error(f"Tourist spot {tourist_spot_id} not found")
        raise HTTPException(status_code=404, detail="Tourist spot not found")
    return db_tourist_spot


@router_v1.put("/{tourist_spot_id}", response_model=schemas.TouristSpot)
async def update_tourist_spot(
    tourist_spot_id: int,
    tourist_spot: schemas.TouristSpotUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await cruds.update_tourist_spot(
        db=db, tourist_spot=tourist_spot, tourist_spot_id=tourist_spot_id
    )


@router_v1.delete("/{tourist_spot_id}", response_model=schemas.TouristSpot)
async def delete_tourist_spot(tourist_spot_id: int, db: AsyncSession = Depends(get_db)):
    success = await cruds.delete_tourist_spot(db=db, tourist_spot_id=tourist_spot_id)
    if not success:
        logger.error(f"Tourist_spot {tourist_spot_id} not found")
        raise HTTPException(status_code=404, detail="Tourist_spot not found")
    # 204 No Content ステータスコードを返すためにレスポンスボディは空
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router_v1.get(
    "/{tourist_spot_id}/articles", response_model=List[schemas.ArticleTouristSpot]
)
async def read_associated_articles(
    tourist_spot_id: int, db: AsyncSession = Depends(get_db)
):
    return await cruds.get_assosicated_articles(db, tourist_spot_id=tourist_spot_id)


@router_v1.post(
    "/{tourist_spot_id}/articles/{article_id}",
    response_model=schemas.ArticleTouristSpot,
)
async def create_link_article_to_tourist_spot(
    tourist_spot_id: int, article_id: int, db: AsyncSession = Depends(get_db)
):
    return await cruds.link_article_to_tourist_spot(
        db, tourist_spot_id=tourist_spot_id, article_id=article_id
    )


@router_v1.delete(
    "/{tourist_spot_id}/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_link_article_from_tourist_spot(
    tourist_spot_id: int, article_id: int, db: AsyncSession = Depends(get_db)
):
    success = await cruds.unlink_article_from_tourist_spot(
        db, tourist_spot_id=tourist_spot_id, article_id=article_id
    )
    if success:
        return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)
    else:
        logger.error(
            f"Association between tourist spot {tourist_spot_id} and article {article_id} not found"
        )
        raise HTTPException(status_code=404, detail="Association not found")


@router_v1.put(
    "/{tourist_spot_id}/articles/{article_id}",
    response_model=schemas.ArticleTouristSpot,
)
async def update_association(
    tourist_spot_id: int, article_id: int, db: AsyncSession = Depends(get_db)
):
    return await cruds.update_article_tourist_spot_association(
        db, tourist_spot_id=tourist_spot_id, article_id=article_id
    )
