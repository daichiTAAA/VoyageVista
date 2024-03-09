from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import cruds, schemas
from db import SessionLocal

router = APIRouter(
    prefix="/translations",
    tags=["translations"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Translation)
def create_translation(
    translation: schemas.TranslationCreate,
    article_id: int,
    db: Session = Depends(get_db),
):
    return cruds.create_translation(
        db=db, translation=translation, article_id=article_id
    )


@router.get("/", response_model=List[schemas.Translation])
def read_translations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    translations = cruds.get_translations(db, skip=skip, limit=limit)
    return translations


@router.get("/{translation_id}", response_model=schemas.Translation)
def read_translation(translation_id: int, db: Session = Depends(get_db)):
    db_translation = cruds.get_translation(db, translation_id=translation_id)
    if db_translation is None:
        raise HTTPException(status_code=404, detail="Translation not found")
    return db_translation


@router.put("/{translation_id}", response_model=schemas.Translation)
def update_translation(
    translation_id: int,
    translation: schemas.TranslationCreate,
    db: Session = Depends(get_db),
):
    db_translation = cruds.get_translation(db, translation_id=translation_id)
    if db_translation is None:
        raise HTTPException(status_code=404, detail="Translation not found")
    return cruds.update_translation(
        db=db, translation=translation, translation_id=translation_id
    )


@router.delete("/{translation_id}", response_model=schemas.Translation)
def delete_translation(translation_id: int, db: Session = Depends(get_db)):
    db_translation = cruds.get_translation(db, translation_id=translation_id)
    if db_translation is None:
        raise HTTPException(status_code=404, detail="Translation not found")
    return cruds.delete_translation(db=db, translation_id=translation_id)
