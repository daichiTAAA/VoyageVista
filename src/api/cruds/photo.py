import os
from sqlalchemy.orm import Session
from fastapi import UploadFile

import models, schemas


def get_photo(db: Session, photo_id: int):
    return db.query(models.Photo).filter(models.Photo.id == photo_id).first()


def get_photos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Photo).offset(skip).limit(limit).all()


async def create_photo(db: Session, photo: UploadFile, article_id: int):
    file_path = f"photos/{photo.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await photo.read())

    db_photo = models.Photo(file_path=file_path, article_id=article_id)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo


async def update_photo(db: Session, photo: UploadFile, photo_id: int):
    db_photo = get_photo(db, photo_id)
    if db_photo:
        file_path = f"photos/{photo.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await photo.read())

        db_photo.file_path = file_path
        db.commit()
        db.refresh(db_photo)
    return db_photo


def delete_photo(db: Session, photo_id: int):
    db_photo = get_photo(db, photo_id)
    if db_photo:
        file_path = db_photo.file_path
        if os.path.exists(file_path):
            os.remove(file_path)
        db.delete(db_photo)
        db.commit()
    return db_photo


def get_photos_by_article(
    db: Session, article_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Photo)
        .filter(models.Photo.article_id == article_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
