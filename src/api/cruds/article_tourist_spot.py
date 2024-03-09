from datetime import datetime

from sqlalchemy.orm import Session

import models, schemas


def get_assosicated_articles(db: Session, tourist_spot_id: int):
    return (
        db.query(models.ArticleTouristSpot)
        .filter(models.ArticleTouristSpot.tourist_spot_id == tourist_spot_id)
        .all()
    )


def link_article_to_tourist_spot(db: Session, tourist_spot_id: int, article_id: int):
    association = models.ArticleTouristSpot(
        article_id=article_id, tourist_spot_id=tourist_spot_id
    )
    db.add(association)
    db.commit()
    return association


def unlink_article_from_tourist_spot(
    db: Session, tourist_spot_id: int, article_id: int
):
    association = (
        db.query(models.ArticleTouristSpot)
        .filter(
            models.ArticleTouristSpot.article_id == article_id,
            models.ArticleTouristSpot.tourist_spot_id == tourist_spot_id,
        )
        .first()
    )
    if association:
        db.delete(association)
        db.commit()
        return True
    return False


def update_article_tourist_spot_association(
    db: Session, tourist_spot_id: int, article_id: int
):
    association = (
        db.query(models.ArticleTouristSpot)
        .filter(
            models.ArticleTouristSpot.article_id == article_id,
            models.ArticleTouristSpot.tourist_spot_id == tourist_spot_id,
        )
        .first()
    )
    if association:
        association.updated_at = datetime.now()
        db.commit()
        return association
    return None
