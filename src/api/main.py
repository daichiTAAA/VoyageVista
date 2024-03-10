from fastapi import FastAPI

import migrate_db
from api.routers import (
    user,
    article,
    photo,
    translation,
    tourist_spot,
    restaurant,
    feedback,
    cultural_insight,
)

app = FastAPI()

app.include_router(user.router_v1, prefix="/v1")
app.include_router(article.router_v1, prefix="/v1")
app.include_router(photo.router_v1, prefix="/v1")
app.include_router(translation.router_v1, prefix="/v1")
app.include_router(tourist_spot.router_v1, prefix="/v1")
app.include_router(restaurant.router_v1, prefix="/v1")
app.include_router(feedback.router_v1, prefix="/v1")
app.include_router(cultural_insight.router_v1, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to the Japan Tourism Info API"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    # from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    # from sqlalchemy.orm import sessionmaker
    # from typing import AsyncGenerator

    # from api.db import get_db, Base

    # ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"

    # async def async_session() -> AsyncGenerator[AsyncSession, None]:
    #     async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    #     async_session = sessionmaker(
    #         autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    #     )

    #     async with async_engine.begin() as conn:
    #         await conn.run_sync(Base.metadata.drop_all)
    #         await conn.run_sync(Base.metadata.create_all)

    #     async with async_session() as session:
    #         yield session

    # async def get_test_db():
    #     yield async_session

    # app.dependency_overrides[get_db] = get_test_db
    # # migrate_db.reset_database()
    # # migrate_db.create_database()
    uvicorn.run("main:app", host="0.0.0.0", port=8100, log_level="info", reload=True)
