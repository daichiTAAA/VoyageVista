from datetime import datetime

from sqlalchemy.orm import Session

import models, schemas


def get_restaurant(db: Session, restaurant_id: int):
    return (
        db.query(models.Restaurant)
        .filter(models.Restaurant.id == restaurant_id)
        .first()
    )


def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Restaurant).offset(skip).limit(limit).all()


def create_restaurant(db: Session, restaurant: schemas.RestaurantCreate):
    db_restaurant = models.Restaurant(**restaurant.model_dump())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


def update_restaurant(
    db: Session, restaurant: schemas.RestaurantUpdate, restaurant_id: int
):
    db_restaurant = get_restaurant(db, restaurant_id)
    if db_restaurant:
        update_data = restaurant.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_restaurant, key, value)
        db.commit()
        db.refresh(db_restaurant)
    return db_restaurant


def delete_restaurant(db: Session, restaurant_id: int):
    db_restaurant = get_restaurant(db, restaurant_id)
    if db_restaurant:
        db.delete(db_restaurant)
        db.commit()
    return db_restaurant


def search_restaurants(db: Session, keyword: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Restaurant)
        .filter(
            models.Restaurant.name.contains(keyword)
            | models.Restaurant.location.contains(keyword)
            | models.Restaurant.cuisine.contains(keyword)
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
