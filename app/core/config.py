from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RAG AI System"
    app_version: str = "0.1.0"
    environment: str = "development"

    chunk_size: int = 500
    chunk_overlap: int = 100

    database_url: str = "postgresql://postgres:postgres@localhost:5433/rag_ai_db"

    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()