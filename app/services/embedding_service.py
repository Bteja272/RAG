from sentence_transformers import SentenceTransformer

from app.core.config import settings


class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        if cls._model is None:
            cls._model = SentenceTransformer(settings.embedding_model_name)
        return cls._model

    @classmethod
    def embed_text(cls, text: str) -> list[float]:
        model = cls.get_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    @classmethod
    def embed_texts(cls, texts: list[str]) -> list[list[float]]:
        model = cls.get_model()
        embeddings = model.encode(texts, convert_to_numpy=True)
        return [embedding.tolist() for embedding in embeddings]