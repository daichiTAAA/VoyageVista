from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import cruds, schemas
from db import SessionLocal

router_v1 = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


@router_v1.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await cruds.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db=db, user=user)


@router_v1.get("/", response_model=List[schemas.User])
async def read_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    users = await cruds.get_users(db, skip=skip, limit=limit)
    return users


@router_v1.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await cruds.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router_v1.put("/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int, user: schemas.UserCreate, db: AsyncSession = Depends(get_db)
):
    db_user = await cruds.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await update_user(db=db, user=user, user_id=user_id)


@router_v1.delete("/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await cruds.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await delete_user(db=db, user_id=user_id)


@router_v1.get("/{user_id}/articles/", response_model=List[schemas.Article])
async def read_user_articles(
    user_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    db_user = await cruds.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    articles = await cruds.get_articles_by_user(
        db=db, user_id=user_id, skip=skip, limit=limit
    )
    return articles
