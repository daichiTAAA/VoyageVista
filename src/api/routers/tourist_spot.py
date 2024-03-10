from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import cruds
from db import SessionLocal
from schemas import TouristSpot as TouristSpotSchema, ArticleTouristSpot
from setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)

router_v1 = APIRouter(
    prefix="/tourist_spots",
    tags=["tourist_spots"],
    responses={404: {"description": "Not found"}},
)


async def get_db():
    async with SessionLocal() as session:
        yield session


@router_v1.post("/", response_model=TouristSpotSchema)
async def create_tourist_spot(
    tourist_spot: TouristSpotSchema, db: AsyncSession = Depends(get_db)
):
    return await cruds.create_tourist_spot(db=db, tourist_spot=tourist_spot)


@router_v1.get("/", response_model=List[TouristSpotSchema])
async def read_tourist_spots(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await cruds.get_tourist_spots(db, skip=skip, limit=limit)


@router_v1.get("/{tourist_spot_id}", response_model=TouristSpotSchema)
async def read_tourist_spot(tourist_spot_id: int, db: AsyncSession = Depends(get_db)):
    db_tourist_spot = await cruds.get_tourist_spot(db, tourist_spot_id=tourist_spot_id)
    if db_tourist_spot is None:
        logger.error(f"Tourist spot {tourist_spot_id} not found")
        raise HTTPException(status_code=404, detail="Tourist spot not found")
    return db_tourist_spot


@router_v1.put("/{tourist_spot_id}", response_model=TouristSpotSchema)
async def update_tourist_spot(
    tourist_spot_id: int,
    tourist_spot: TouristSpotSchema,
    db: AsyncSession = Depends(get_db),
):
    return await cruds.update_tourist_spot(
        db=db, tourist_spot=tourist_spot, tourist_spot_id=tourist_spot_id
    )


@router_v1.delete("/{tourist_spot_id}", response_model=TouristSpotSchema)
async def delete_tourist_spot(tourist_spot_id: int, db: AsyncSession = Depends(get_db)):
    return await cruds.delete_tourist_spot(db=db, tourist_spot_id=tourist_spot_id)


@router_v1.get("/{tourist_spot_id}/articles", response_model=List[ArticleTouristSpot])
async def read_associated_articles(
    tourist_spot_id: int, db: AsyncSession = Depends(get_db)
):
    return await cruds.get_assosicated_articles(db, tourist_spot_id=tourist_spot_id)


@router_v1.post(
    "/{tourist_spot_id}/articles/{article_id}", response_model=ArticleTouristSpot
)
async def create_link_article_to_tourist_spot(
    tourist_spot_id: int, article_id: int, db: AsyncSession = Depends(get_db)
):
    return await cruds.link_article_to_tourist_spot(
        db, tourist_spot_id=tourist_spot_id, article_id=article_id
    )


@router_v1.delete("/{tourist_spot_id}/articles/{article_id}", response_model=dict)
async def delete_link_article_from_tourist_spot(
    tourist_spot_id: int, article_id: int, db: AsyncSession = Depends(get_db)
):
    success = await cruds.unlink_article_from_tourist_spot(
        db, tourist_spot_id=tourist_spot_id, article_id=article_id
    )
    if success:
        return {"message": "Association deleted successfully"}
    else:
        logger.error(
            f"Association between tourist spot {tourist_spot_id} and article {article_id} not found"
        )
        raise HTTPException(status_code=404, detail="Association not found")


@router_v1.put(
    "/{tourist_spot_id}/articles/{article_id}", response_model=ArticleTouristSpot
)
async def update_association(
    tourist_spot_id: int, article_id: int, db: AsyncSession = Depends(get_db)
):
    return await cruds.update_article_tourist_spot_association(
        db, tourist_spot_id=tourist_spot_id, article_id=article_id
    )
