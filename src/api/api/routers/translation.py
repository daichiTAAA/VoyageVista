from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import api.cruds as cruds
from api.db import get_db
import api.schemas as schemas
from api.setup_logger import setup_logger

logger, log_decorator = setup_logger(__name__)

router_v1 = APIRouter(
    prefix="/translations",
    tags=["translations"],
    responses={404: {"description": "Not found"}},
)


@router_v1.post(
    "/", response_model=schemas.Translation, status_code=status.HTTP_201_CREATED
)
async def create_translation(
    translation: schemas.TranslationCreate,
    article_id: int,
    db: AsyncSession = Depends(get_db),
):
    db_translation = await cruds.create_translation(
        db=db, translation=translation, article_id=article_id
    )
    if not db_translation:
        logger.error("Translation could not be created")
        raise HTTPException(status_code=400, detail="Translation could not be created")
    return db_translation


@router_v1.get("/", response_model=List[schemas.Translation])
async def read_translations(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await cruds.get_translations(db, skip=skip, limit=limit)


@router_v1.get("/{translation_id}", response_model=schemas.Translation)
async def read_translation(translation_id: int, db: AsyncSession = Depends(get_db)):
    db_translation = await cruds.get_translation(db, translation_id=translation_id)
    if db_translation is None:
        logger.error(f"Translation {translation_id} not found")
        raise HTTPException(status_code=404, detail="Translation not found")
    return db_translation


@router_v1.put("/{translation_id}", response_model=schemas.Translation)
async def update_translation(
    translation_id: int,
    translation: schemas.TranslationUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await cruds.update_translation(
        db=db, translation=translation, translation_id=translation_id
    )


@router_v1.delete("/{translation_id}", response_model=schemas.Translation)
async def delete_translation(translation_id: int, db: AsyncSession = Depends(get_db)):
    success = await cruds.delete_translation(db=db, translation_id=translation_id)
    if not success:
        logger.error(f"translation {translation_id} not found")
        raise HTTPException(status_code=404, detail="translation not found")
    # 204 No Content ステータスコードを返すためにレスポンスボディは空
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)
