from datetime import datetime

from sqlalchemy.orm import Session

import models, schemas


def get_tourist_spot(db: Session, tourist_spot_id: int):
    return (
        db.query(models.TouristSpot)
        .filter(models.TouristSpot.id == tourist_spot_id)
        .first()
    )


def get_tourist_spots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TouristSpot).offset(skip).limit(limit).all()


def create_tourist_spot(db: Session, tourist_spot: schemas.TouristSpotCreate):
    db_tourist_spot = models.TouristSpot(**tourist_spot.model_dump())
    db.add(db_tourist_spot)
    db.commit()
    db.refresh(db_tourist_spot)
    return db_tourist_spot


def update_tourist_spot(
    db: Session, tourist_spot: schemas.TouristSpotUpdate, tourist_spot_id: int
):
    db_tourist_spot = get_tourist_spot(db, tourist_spot_id)
    if db_tourist_spot:
        update_data = tourist_spot.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tourist_spot, key, value)
        db.commit()
        db.refresh(db_tourist_spot)
    return db_tourist_spot


def delete_tourist_spot(db: Session, tourist_spot_id: int):
    db_tourist_spot = get_tourist_spot(db, tourist_spot_id)
    if db_tourist_spot:
        db.delete(db_tourist_spot)
        db.commit()
    return db_tourist_spot


def search_tourist_spots(db: Session, keyword: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.TouristSpot)
        .filter(
            models.TouristSpot.name.contains(keyword)
            | models.TouristSpot.location.contains(keyword)
            | models.TouristSpot.description.contains(keyword)
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
