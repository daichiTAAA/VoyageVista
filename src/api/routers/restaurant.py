from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import cruds, schemas
from db import SessionLocal
from setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)

router_v1 = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
    responses={404: {"description": "Not found"}},
)


async def get_db():
    async with SessionLocal() as session:
        yield session


@router_v1.post("/", response_model=schemas.Restaurant)
async def create_restaurant(
    restaurant: schemas.RestaurantCreate, db: AsyncSession = Depends(get_db)
):
    return await cruds.create_restaurant(db=db, restaurant=restaurant)


@router_v1.get("/", response_model=List[schemas.Restaurant])
async def read_restaurants(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await cruds.get_restaurants(db, skip=skip, limit=limit)


@router_v1.get("/{restaurant_id}", response_model=schemas.Restaurant)
async def read_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    db_restaurant = await cruds.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        logger.error(f"Restaurant {restaurant_id} not found")
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant


@router_v1.put("/{restaurant_id}", response_model=schemas.Restaurant)
async def update_restaurant(
    restaurant_id: int,
    restaurant: schemas.RestaurantCreate,
    db: AsyncSession = Depends(get_db),
):
    db_restaurant = await cruds.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        logger.error(f"Restaurant {restaurant_id} not found")
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return await cruds.update_restaurant(
        db=db, restaurant=restaurant, restaurant_id=restaurant_id
    )


@router_v1.delete("/{restaurant_id}", response_model=schemas.Restaurant)
async def delete_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await cruds.delete_restaurant(db=db, restaurant_id=restaurant_id)


@router_v1.get(
    "/{restaurant_id}/articles", response_model=List[schemas.ArticleRestaurant]
)
async def read_associated_articles(
    restaurant_id: int, db: AsyncSession = Depends(get_db)
):
    return await cruds.get_associated_articles(db, restaurant_id=restaurant_id)


@router_v1.post(
    "/{restaurant_id}/articles/{article_id}", response_model=schemas.ArticleRestaurant
)
async def create_link_article_to_restaurant(
    restaurant_id: int, article_id: int, db: AsyncSession = Depends(get_db)
):
    return await cruds.link_article_to_restaurant(
        db, restaurant_id=restaurant_id, article_id=article_id
    )


@router_v1.delete("/{restaurant_id}/articles/{article_id}", response_model=dict)
async def delete_link_article_to_restaurant(
    restaurant_id: int, article_id: int, db: AsyncSession = Depends(get_db)
):
    success = await cruds.unlink_article_from_restaurant(
        db, restaurant_id=restaurant_id, article_id=article_id
    )
    if success:
        return {"message": "Association deleted successfully"}
    else:
        logger.error(
            f"Association between restaurant {restaurant_id} and article {article_id} not found"
        )
        raise HTTPException(status_code=404, detail="Association not found")


@router_v1.put(
    "/{restaurant_id}/articles/{article_id}", response_model=schemas.ArticleRestaurant
)
async def update_association(
    restaurant_id: int, article_id: int, db: AsyncSession = Depends(get_db)
):
    association = await cruds.update_article_restaurant_association(
        db, restaurant_id=restaurant_id, article_id=article_id
    )
    if association:
        return association
    else:
        logger.error(
            f"Association between restaurant {restaurant_id} and article {article_id} not found"
        )
        raise HTTPException(status_code=404, detail="Association not found")
