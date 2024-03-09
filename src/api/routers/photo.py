from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

import cruds, schemas
from db import SessionLocal

router = APIRouter(
    prefix="/photos",
    tags=["photos"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Photo)
def create_photo(
    photo: UploadFile = File(...), article_id: int = None, db: Session = Depends(get_db)
):
    return cruds.create_photo(db=db, photo=photo, article_id=article_id)


@router.get("/", response_model=List[schemas.Photo])
def read_photos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    photos = cruds.get_photos(db, skip=skip, limit=limit)
    return photos


@router.get("/{photo_id}", response_model=schemas.Photo)
def read_photo(photo_id: int, db: Session = Depends(get_db)):
    db_photo = cruds.get_photo(db, photo_id=photo_id)
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return db_photo


@router.put("/{photo_id}", response_model=schemas.Photo)
def update_photo(
    photo_id: int, photo: UploadFile = File(...), db: Session = Depends(get_db)
):
    db_photo = cruds.get_photo(db, photo_id=photo_id)
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return cruds.update_photo(db=db, photo=photo, photo_id=photo_id)


@router.delete("/{photo_id}", response_model=schemas.Photo)
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    db_photo = cruds.get_photo(db, photo_id=photo_id)
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return cruds.delete_photo(db=db, photo_id=photo_id)
