from datetime import datetime
from sqlalchemy.orm import Session

import models, schemas
from security import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.hashed_password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserCreate, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user.model_dump(exclude_unset=True)
        if "hashed_password" in update_data:
            update_data["hashed_password"] = get_password_hash(user.hashed_password)
            del update_data["password"]
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def get_articles_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Article)
        .filter(models.Article.author_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
