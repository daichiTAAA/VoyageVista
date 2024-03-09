from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import cruds, schemas
from db import SessionLocal

router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Restaurant)
def create_restaurant(
    restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)
):
    return cruds.create_restaurant(db=db, restaurant=restaurant)


@router.get("/", response_model=List[schemas.Restaurant])
def read_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    restaurants = cruds.get_restaurants(db, skip=skip, limit=limit)
    return restaurants


@router.get("/{restaurant_id}", response_model=schemas.Restaurant)
def read_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = cruds.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant


@router.put("/{restaurant_id}", response_model=schemas.Restaurant)
def update_restaurant(
    restaurant_id: int,
    restaurant: schemas.RestaurantCreate,
    db: Session = Depends(get_db),
):
    db_restaurant = cruds.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return cruds.update_restaurant(
        db=db, restaurant=restaurant, restaurant_id=restaurant_id
    )


@router.delete("/{restaurant_id}", response_model=schemas.Restaurant)
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = cruds.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return cruds.delete_restaurant(db=db, restaurant_id=restaurant_id)


@router.get("/{restaurant_id}/articles", response_model=List[schemas.ArticleRestaurant])
def read_associated_articles(restaurant_id: int, db: Session = Depends(get_db)):
    articles = cruds.get_assosicated_articles(db, restaurant_id=restaurant_id)
    return articles


@router.post(
    "/{restaurant_id}/articles/{article_id}", response_model=schemas.ArticleRestaurant
)
def create_link_article_to_restaurant(
    restaurant_id: int, article_id: int, db: Session = Depends(get_db)
):
    try:
        association = cruds.link_article_to_restaurant(
            db, restaurant_id=restaurant_id, article_id=article_id
        )
        return association
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{restaurant_id}/articles/{article_id}", response_model=dict)
def delete_link_article_to_restaurant(
    restaurant_id: int, article_id: int, db: Session = Depends(get_db)
):
    success = cruds.unlink_article_from_restaurant(
        db, restaurant_id=restaurant_id, article_id=article_id
    )
    if success:
        return {"message": "Association deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Association not found")


@router.put(
    "/{restaurant_id}/articles/{article_id}", response_model=schemas.ArticleRestaurant
)
def update_association(
    restaurant_id: int, article_id: int, db: Session = Depends(get_db)
):
    association = cruds.update_article_restaurant_association(
        db, restaurant_id=restaurant_id, article_id=article_id
    )
    if association:
        return association
    else:
        raise HTTPException(status_code=404, detail="Association not found")
