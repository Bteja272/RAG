from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.query import router as query_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.include_router(health_router)
app.include_router(query_router)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} API is running",
        "environment": settings.environment,
    }