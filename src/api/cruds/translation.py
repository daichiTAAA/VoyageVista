from sqlalchemy.orm import Session

import models, schemas


def get_translation(db: Session, translation_id: int):
    return (
        db.query(models.Translation)
        .filter(models.Translation.id == translation_id)
        .first()
    )


def get_translations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Translation).offset(skip).limit(limit).all()


def create_translation(
    db: Session, translation: schemas.TranslationCreate, article_id: int
):
    db_translation = models.Translation(
        **translation.model_dump(), article_id=article_id
    )
    db.add(db_translation)
    db.commit()
    db.refresh(db_translation)
    return db_translation


def update_translation(
    db: Session, translation: schemas.TranslationUpdate, translation_id: int
):
    db_translation = get_translation(db, translation_id)
    if db_translation:
        update_data = translation.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_translation, key, value)
        db.commit()
        db.refresh(db_translation)
    return db_translation


def delete_translation(db: Session, translation_id: int):
    db_translation = get_translation(db, translation_id)
    if db_translation:
        db.delete(db_translation)
        db.commit()
    return db_translation


def get_translations_by_article(
    db: Session, article_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Translation)
        .filter(models.Translation.article_id == article_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_translation_by_article_and_language(
    db: Session, article_id: int, language: str
):
    return (
        db.query(models.Translation)
        .filter(
            models.Translation.article_id == article_id,
            models.Translation.language == language,
        )
        .first()
    )
