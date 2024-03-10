from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import cruds
from db import SessionLocal
from schemas import Translation

router_v1 = APIRouter(
    prefix="/translations",
    tags=["translations"],
    responses={404: {"description": "Not found"}},
)


async def get_db():
    async with SessionLocal() as session:
        yield session


@router_v1.post("/", response_model=Translation)
async def create_translation(
    translation: Translation, article_id: int, db: AsyncSession = Depends(get_db)
):
    return await cruds.create_translation(
        db=db, translation=translation, article_id=article_id
    )


@router_v1.get("/", response_model=List[Translation])
async def read_translations(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await cruds.get_translations(db, skip=skip, limit=limit)


@router_v1.get("/{translation_id}", response_model=Translation)
async def read_translation(translation_id: int, db: AsyncSession = Depends(get_db)):
    db_translation = await cruds.get_translation(db, translation_id=translation_id)
    if db_translation is None:
        raise HTTPException(status_code=404, detail="Translation not found")
    return db_translation


@router_v1.put("/{translation_id}", response_model=Translation)
async def update_translation(
    translation_id: int, translation: Translation, db: AsyncSession = Depends(get_db)
):
    return await cruds.update_translation(
        db=db, translation=translation, translation_id=translation_id
    )


@router_v1.delete("/{translation_id}", response_model=Translation)
async def delete_translation(translation_id: int, db: AsyncSession = Depends(get_db)):
    return await cruds.delete_translation(db=db, translation_id=translation_id)
