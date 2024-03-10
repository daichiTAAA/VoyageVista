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

app.include_router(user.router_v1, prefix="/v1")
app.include_router(article.router_v1, prefix="/v1")
app.include_router(photo.router_v1, prefix="/v1")
app.include_router(translation.router_v1, prefix="/v1")
app.include_router(tourist_spot.router_v1, prefix="/v1")
app.include_router(restaurant.router_v1, prefix="/v1")
app.include_router(feedback.router_v1, prefix="/v1")
app.include_router(cultural_insight.router_v1, prefix="/v1")


if __name__ == "__main__":
    import uvicorn

    # migrate_db.reset_database()
    migrate_db.create_database()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
