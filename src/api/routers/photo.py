from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import cruds, schemas
from db import SessionLocal
from setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)

router_v1 = APIRouter(
    prefix="/photos",
    tags=["photos"],
    responses={404: {"description": "Not found"}},
)


async def get_db():
    async with SessionLocal() as session:
        yield session


@router_v1.post("/", response_model=schemas.Photo)
async def create_photo(
    photo: UploadFile = File(...),
    article_id: int = None,
    db: AsyncSession = Depends(get_db),
):
    return await cruds.create_photo(db=db, photo=photo, article_id=article_id)


@router_v1.get("/", response_model=List[schemas.Photo])
async def read_photos(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    photos = await cruds.get_photos(db, skip=skip, limit=limit)
    return photos


@router_v1.get("/{photo_id}", response_model=schemas.Photo)
async def read_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
    db_photo = await cruds.get_photo(db, photo_id=photo_id)
    if db_photo is None:
        logger.error(f"Photo {photo_id} not found")
        raise HTTPException(status_code=404, detail="Photo not found")
    return db_photo


@router_v1.put("/{photo_id}", response_model=schemas.Photo)
async def update_photo(
    photo_id: int, photo: UploadFile = File(...), db: AsyncSession = Depends(get_db)
):
    db_photo = await cruds.get_photo(db, photo_id=photo_id)
    if db_photo is None:
        logger.error(f"Photo {photo_id} not found")
        raise HTTPException(status_code=404, detail="Photo not found")
    return await cruds.update_photo(db=db, photo=photo, photo_id=photo_id)


@router_v1.delete("/{photo_id}", response_model=schemas.Photo)
async def delete_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
    db_photo = await cruds.get_photo(db, photo_id=photo_id)
    if db_photo is None:
        logger.error(f"Photo {photo_id} not found")
        raise HTTPException(status_code=404, detail="Photo not found")
    return await cruds.delete_photo(db=db, photo_id=photo_id)
