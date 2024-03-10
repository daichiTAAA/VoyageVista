from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas
from security import get_password_hash


# ユーザーをIDで取得
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()


# ユーザーをEメールで取得
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()


# 複数のユーザーを取得
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()


# ユーザーの作成
async def create_user(db: AsyncSession, user: schemas.UserCreate):
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
    await db.commit()
    await db.refresh(db_user)
    return db_user


# ユーザー情報の更新
async def update_user(db: AsyncSession, user: schemas.UserCreate, user_id: int):
    db_user = await get_user(db, user_id)
    if db_user:
        update_data = user.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]
        for key, value in update_data.items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user


# ユーザーの削除
async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user


# 特定ユーザーの記事を取得
async def get_articles_by_user(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
):
    result = await db.execute(
        select(models.Article)
        .filter(models.Article.author_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
