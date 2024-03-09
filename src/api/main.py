from fastapi import FastAPI

import migrate_db
from routers import (
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

app.include_router(user.router)
app.include_router(article.router)
app.include_router(photo.router)
app.include_router(translation.router)
app.include_router(tourist_spot.router)
app.include_router(restaurant.router)
app.include_router(feedback.router)
app.include_router(cultural_insight.router)


if __name__ == "__main__":
    import uvicorn

    # migrate_db.reset_database()
    migrate_db.create_database()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
