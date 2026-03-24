from fastapi import FastAPI
from app.api.routes.health import router as health_router

app = FastAPI(title="RAG AI System", version="0.1.0")

app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "RAG AI System API is running"}