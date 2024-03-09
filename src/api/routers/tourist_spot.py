from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import cruds, schemas
from db import SessionLocal

router = APIRouter(
    prefix="/tourist_spots",
    tags=["tourist_spots"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.TouristSpot)
def create_tourist_spot(
    tourist_spot: schemas.TouristSpotCreate, db: Session = Depends(get_db)
):
    return cruds.create_tourist_spot(db=db, tourist_spot=tourist_spot)


@router.get("/", response_model=List[schemas.TouristSpot])
def read_tourist_spots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tourist_spots = cruds.get_tourist_spots(db, skip=skip, limit=limit)
    return tourist_spots


@router.get("/{tourist_spot_id}", response_model=schemas.TouristSpot)
def read_tourist_spot(tourist_spot_id: int, db: Session = Depends(get_db)):
    db_tourist_spot = cruds.get_tourist_spot(db, tourist_spot_id=tourist_spot_id)
    if db_tourist_spot is None:
        raise HTTPException(status_code=404, detail="Tourist spot not found")
    return db_tourist_spot


@router.put("/{tourist_spot_id}", response_model=schemas.TouristSpot)
def update_tourist_spot(
    tourist_spot_id: int,
    tourist_spot: schemas.TouristSpotCreate,
    db: Session = Depends(get_db),
):
    db_tourist_spot = cruds.get_tourist_spot(db, tourist_spot_id=tourist_spot_id)
    if db_tourist_spot is None:
        raise HTTPException(status_code=404, detail="Tourist spot not found")
    return cruds.update_tourist_spot(
        db=db, tourist_spot=tourist_spot, tourist_spot_id=tourist_spot_id
    )


@router.delete("/{tourist_spot_id}", response_model=schemas.TouristSpot)
def delete_tourist_spot(tourist_spot_id: int, db: Session = Depends(get_db)):
    db_tourist_spot = cruds.get_tourist_spot(db, tourist_spot_id=tourist_spot_id)
    if db_tourist_spot is None:
        raise HTTPException(status_code=404, detail="Tourist spot not found")
    return cruds.delete_tourist_spot(db=db, tourist_spot_id=tourist_spot_id)


@router.get(
    "/{tourist_spot_id}/articles", response_model=List[schemas.ArticleTouristSpot]
)
def read_associated_articles(tourist_spot_id: int, db: Session = Depends(get_db)):
    articles = cruds.get_assosicated_articles(db, tourist_spot_id=tourist_spot_id)
    return articles


@router.post(
    "/{tourist_spot_id}/articles/{article_id}",
    response_model=schemas.ArticleTouristSpot,
)
def create_link_article_to_tourist_spot(
    tourist_spot_id: int, article_id: int, db: Session = Depends(get_db)
):
    try:
        association = cruds.link_article_to_tourist_spot(
            db, tourist_spot_id=tourist_spot_id, article_id=article_id
        )
        return association
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{tourist_spot_id}/articles/{article_id}", response_model=dict)
def delete_link_article_from_tourist_spot(
    tourist_spot_id: int, article_id: int, db: Session = Depends(get_db)
):
    success = cruds.unlink_article_from_tourist_spot(
        db, tourist_spot_id=tourist_spot_id, article_id=article_id
    )
    if success:
        return {"message": "Association deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Association not found")


@router.put(
    "/{tourist_spot_id}/articles/{article_id}",
    response_model=schemas.ArticleTouristSpot,
)
def update_association(
    tourist_spot_id: int, article_id: int, db: Session = Depends(get_db)
):
    association = cruds.update_article_tourist_spot_association(
        db, tourist_spot_id=tourist_spot_id, article_id=article_id
    )
    if association:
        return association
    else:
        raise HTTPException(status_code=404, detail="Association not found")
