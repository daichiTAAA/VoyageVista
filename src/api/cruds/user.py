from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, schemas
from security import get_password_hash
from setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)


# ユーザーをIDで取得
async def get_user(db: AsyncSession, user_id: int):
    logger.info(f"Fetching user with ID {user_id}")
    try:
        result = await db.execute(select(models.User).filter(models.User.id == user_id))
        logger.info(f"Successfully fetched user with ID {user_id}")
        return result.scalars().first()
    except Exception as e:
        logger.error(f"Error in get_user: {e}")
        return None


# ユーザーをEメールで取得
async def get_user_by_email(db: AsyncSession, email: str):
    logger.info(f"Fetching user with email {email}")
    try:
        result = await db.execute(
            select(models.User).filter(models.User.email == email)
        )
        logger.info(f"Successfully fetched user with email {email}")
        return result.scalars().first()
    except Exception as e:
        logger.error(f"Error in get_user_by_email: {e}")
        return None


# 複数のユーザーを取得
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching users with skip {skip} and limit {limit}")
    try:
        result = await db.execute(select(models.User).offset(skip).limit(limit))
        logger.info(f"Successfully fetched users with skip {skip} and limit {limit}")
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Error in get_users: {e}")
        return []


# ユーザーの作成
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    logger.info(f"Creating user with username {user.username}")
    try:
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
        logger.info(f"Successfully created user with username {user.username}")
        return db_user
    except Exception as e:
        logger.error(f"Error in create_user: {e}")
        return None


# ユーザー情報の更新
async def update_user(db: AsyncSession, user: schemas.UserCreate, user_id: int):
    logger.info(f"Updating user with ID {user_id}")
    try:
        db_user = await get_user(db, user_id)
        if db_user:
            update_data = user.model_dump(exclude_unset=True)
            if "password" in update_data:
                update_data["hashed_password"] = get_password_hash(
                    update_data["password"]
                )
                del update_data["password"]
            for key, value in update_data.items():
                setattr(db_user, key, value)
            await db.commit()
            await db.refresh(db_user)
            logger.info(f"Successfully updated user with ID {user_id}")
        else:
            logger.warning(f"User with ID {user_id} not found")
        return db_user
    except Exception as e:
        logger.error(f"Error in update_user: {e}")
        return None


# ユーザーの削除
async def delete_user(db: AsyncSession, user_id: int):
    logger.info(f"Deleting user with ID {user_id}")
    try:
        db_user = await get_user(db, user_id)
        if db_user:
            await db.delete(db_user)
            await db.commit()
            logger.info(f"Successfully deleted user with ID {user_id}")
        else:
            logger.warning(f"User with ID {user_id} not found")
        return db_user
    except Exception as e:
        logger.error(f"Error in delete_user: {e}")
        return None


# 特定ユーザーの記事を取得
async def get_articles_by_user(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
):
    logger.info(f"Fetching articles by user with ID {user_id}")
    try:
        result = await db.execute(
            select(models.Article)
            .filter(models.Article.author_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        logger.info(f"Successfully fetched articles by user with ID {user_id}")
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Error in get_articles_by_user: {e}")
        return []
